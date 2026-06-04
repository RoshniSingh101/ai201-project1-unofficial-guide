#!/usr/bin/env python3
"""Structure-aware chunker for the cleaned OMSCS corpus.

Chunking strategy: target 200 tokens, 20-token overlap (override with --size /
--overlap), packing whole *lines* so a course row is never split from its
rating/tier.

Hybrid mode (the default; disable with --no-hybrid) picks a strategy per
document type, because one global size can't serve the whole corpus:
  * Spec pages -> "atomic": the whole requirement list (and the "only bold =
    offered online" caveat) stays in one chunk, so the specialization
    questions always retrieve a complete, self-contained list.
  * Difficulty/workload tables -> "sectioned": one tier per chunk, with the
    tier label + column header repeated so each chunk is self-describing.
  * Everything else (comments, prose, CSV sheets) -> "sliding": plain
    overlapping window at the target size.

Each chunk carries its SOURCE/URL as metadata for attribution.

Token counts here are ESTIMATED (~1.3 tokens/word) because the BGE-m3
tokenizer isn't installed in this env; swap in the real tokenizer for
production by replacing `est_tokens`.

Token counts here are ESTIMATED (~1.3 tokens/word) because the BGE-m3
tokenizer isn't installed in this env; swap in the real tokenizer for
production by replacing `est_tokens`.
"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path

CLEAN_DIR = Path(__file__).resolve().parent.parent / "documents" / "clean"

CHUNK_TOKENS = 200
OVERLAP_TOKENS = 20
TOKENS_PER_WORD = 1.3  # rough XLM-RoBERTa/BGE-m3 estimate for English


def est_tokens(text: str) -> int:
    words = len(re.findall(r"\S+", text))
    return max(1, round(words * TOKENS_PER_WORD))


@dataclass
class Chunk:
    source: str
    url: str
    text: str
    tokens: int = field(init=False)

    def __post_init__(self):
        self.tokens = est_tokens(self.text)


def parse(path: Path) -> tuple[str, str, list[str]]:
    """Return (source, url, body_lines) for a cleaned file."""
    lines = path.read_text(encoding="utf-8").splitlines()
    source = url = ""
    body_start = 0
    for i, ln in enumerate(lines[:6]):
        low = ln.lower()
        if low.startswith("source:"):
            source = ln.split(":", 1)[1].strip()
        elif low.startswith("url:"):
            url = ln.split(":", 1)[1].strip()
        if set(ln.strip()) == {"="} and len(ln.strip()) >= 10:
            body_start = i + 1
    body = [ln for ln in lines[body_start:]]
    return source, url, body


# --- table-structure detection (for the header-repeat refinement) -----------
SECTION_RE = re.compile(r"^(tier\b|sub-area\b|core courses\b|electives\b"
                        r"|free electives\b)", re.IGNORECASE)


def is_table_row(line: str) -> bool:
    return "\t" in line


# rank cells sometimes carry annotation prefixes, e.g. "$53", "+2", "*7".
_RANK_PREFIX = "$+*#⬆️↓ \t"


def is_data_row(line: str) -> bool:
    """A tab-delimited row whose first cell is a (possibly annotated) rank #."""
    if not is_table_row(line):
        return False
    first = line.split("\t", 1)[0].strip().lstrip(_RANK_PREFIX)
    return bool(first) and first[:1].isdigit()


def is_header_row(line: str) -> bool:
    """A tab-delimited row that is not a data row (i.e. column labels)."""
    return is_table_row(line) and not is_data_row(line)


def table_context(body: list[str]) -> list[tuple[str, str]]:
    """For each line, the (section_label, header_row) table context in force.

    Lets a chunk that *starts* inside a table re-prepend the tier/section label
    and the column header so split tables stay self-describing.
    """
    ctx: list[tuple[str, str]] = []
    section = header = ""
    for ln in body:
        s = ln.strip()
        if SECTION_RE.match(s):
            section = s
            header = ""  # a new section's header hasn't been seen yet
        elif is_header_row(ln):
            header = ln
        elif s and not is_data_row(ln) and not is_table_row(ln):
            # left the table: a normal prose line clears table context, but
            # keeps a section label (e.g. spec sub-areas span prose + lists)
            header = ""
        ctx.append((section, header))
    return ctx


MAX_ATOMIC_TOKENS = 800  # spec pages below this stay a single chunk


def doc_mode(source: str, url: str) -> str:
    """Pick a chunking strategy per document type (the 'hybrid' decision).

    * "atomic"    – specialization pages: keep the whole requirement list (and
                    the "only bold = offered online" caveat) in one chunk so
                    Q1/Q4/Q5 always retrieve a complete, self-contained list.
    * "sectioned" – ranking tables: cut on tier/section boundaries so each
                    chunk is one self-describing tier (Q2/Q3).
    * "sliding"   – everything else (comments, prose, CSV sheets): plain
                    overlapping window.
    """
    if "omscs.gatech.edu" in url:
        return "atomic"
    if "Difficulty" in source or "Workload" in source:
        return "sectioned"
    return "sliding"


def is_boundary(line: str) -> bool:
    return bool(SECTION_RE.match(line.strip()))


def pack(source: str, url: str, body: list[str], mode: str = "sliding") -> list[Chunk]:
    """Pack whole lines into ~CHUNK_TOKENS chunks with ~OVERLAP_TOKENS overlap.

    `mode` (see doc_mode) tunes the boundary policy:
      * atomic    – emit the whole doc as one chunk if it fits MAX_ATOMIC_TOKENS.
      * sectioned – force a clean break at each tier/section boundary.
      * sliding   – size-based breaks only.

    When a (non-first) chunk begins inside a table, the active section label and
    column header are re-prepended as a "(continued)" block so the rows below
    stay interpretable on their own.
    """
    # Drop leading/trailing blanks but keep internal structure.
    while body and not body[0].strip():
        body.pop(0)
    while body and not body[-1].strip():
        body.pop()
    if not body:
        return []

    if mode == "atomic" and est_tokens("\n".join(body)) <= MAX_ATOMIC_TOKENS:
        return [Chunk(source, url, "\n".join(body).strip())]

    ctx = table_context(body)

    chunks: list[Chunk] = []
    cur: list[tuple[int, str]] = []  # (orig_index, line)
    cur_tok = 0

    def emit():
        if not cur:
            return
        lines = [ln for _, ln in cur]
        # Header-repeat: if this chunk opens inside a table (its first
        # non-blank line is a data/header row) and the column header isn't
        # already present, inject the section label + header at the top.
        if chunks:
            first_idx = next((i for i, (_, ln) in enumerate(cur) if ln.strip()),
                             None)
            if first_idx is not None:
                oidx, fline = cur[first_idx]
                if is_table_row(fline):
                    section, header = ctx[oidx]
                    prefix = lines[:first_idx]  # anything above the first row
                    inject = []
                    if section and section not in prefix:
                        inject.append(section)
                    # a data row needs its column header above it; a header row
                    # is already self-describing.
                    if header and is_data_row(fline) and header not in prefix:
                        inject.append(header)
                    if inject:
                        lines = [*inject, "(continued)", ""] + lines
        text = "\n".join(lines).strip()
        if text and (not chunks or text != chunks[-1].text):
            chunks.append(Chunk(source, url, text))

    def flush():
        nonlocal cur, cur_tok
        if not cur:
            return
        emit()
        # build overlap tail from the end of cur
        tail, t = [], 0
        for item in reversed(cur):
            t += est_tokens(item[1]) if item[1].strip() else 0
            tail.insert(0, item)
            if t >= OVERLAP_TOKENS:
                break
        cur = tail[:]  # carry overlap into next chunk
        cur_tok = sum(est_tokens(l) for _, l in cur if l.strip())

    for i, ln in enumerate(body):
        lt = est_tokens(ln) if ln.strip() else 0
        # sectioned mode: start a fresh chunk at each tier/section boundary
        if (mode == "sectioned" and is_boundary(ln)
                and any(l.strip() for _, l in cur)):
            emit()
            cur, cur_tok = [], 0
        elif cur_tok + lt > CHUNK_TOKENS and cur_tok > OVERLAP_TOKENS:
            flush()
        cur.append((i, ln))
        cur_tok += lt
    emit()
    return chunks


def chunk_corpus(clean_dir: Path = CLEAN_DIR, hybrid: bool = True) -> list[Chunk]:
    out: list[Chunk] = []
    for f in sorted(clean_dir.glob("*.txt")):
        source, url, body = parse(f)
        mode = doc_mode(source, url) if hybrid else "sliding"
        out.extend(pack(source, url, body, mode))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stats", action="store_true", help="print chunk-size distribution")
    ap.add_argument("--print", type=int, default=0, metavar="N",
                    help="print first N chunks")
    ap.add_argument("--size", type=int, help="override chunk size (tokens)")
    ap.add_argument("--overlap", type=int, help="override overlap (tokens)")
    ap.add_argument("--no-hybrid", dest="hybrid", action="store_false",
                    help="disable per-document strategy; use one sliding window "
                         "for every file (hybrid is the default: atomic specs, "
                         "sectioned tables, sliding prose)")
    ap.set_defaults(hybrid=True)
    args = ap.parse_args()

    global CHUNK_TOKENS, OVERLAP_TOKENS
    if args.size:
        CHUNK_TOKENS = args.size
    if args.overlap is not None:
        OVERLAP_TOKENS = args.overlap

    chunks = chunk_corpus(hybrid=args.hybrid)
    print(f"{len(chunks)} chunks from {len(list(CLEAN_DIR.glob('*.txt')))} files "
          f"(target {CHUNK_TOKENS} tok, overlap {OVERLAP_TOKENS})\n")

    if args.stats:
        toks = sorted(c.tokens for c in chunks)
        n = len(toks)
        print(f"tokens/chunk  min={toks[0]} median={toks[n//2]} "
              f"max={toks[-1]} mean={sum(toks)//n}")
        from collections import Counter
        per_src = Counter(c.source for c in chunks)
        print("\nchunks per source:")
        for s, c in per_src.items():
            print(f"  {c:3d}  {s}")

    for i, c in enumerate(chunks[: args.print]):
        print(f"\n{'='*70}\nCHUNK {i} | {c.source} | ~{c.tokens} tok\n{'-'*70}\n{c.text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
