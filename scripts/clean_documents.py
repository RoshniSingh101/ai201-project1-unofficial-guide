#!/usr/bin/env python3
"""Clean scraped documents in documents/raw -> documents/clean.

Removes boilerplate that appears on scraped pages: HTML tags, navigation
menus, cookie/consent banners, ads ("Promoted"), footers, repeated site
headers, "Read more"/share/login links, vote/comment counts, "related
posts" trailers, and copyright lines.

The SOURCE / URL / separator header block at the top of each file is kept,
since it is useful provenance metadata rather than page boilerplate.

Usage:
    python scripts/clean_documents.py            # raw -> clean
    python scripts/clean_documents.py --check    # report only, write nothing
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "documents" / "raw"
CLEAN_DIR = Path(__file__).resolve().parent.parent / "documents" / "clean"

# --- Mojibake repair ---------------------------------------------------------
# The scrape decoded some UTF-8 bytes as latin-1, so emoji/symbols arrive as
# garbled runs like "â\x98\x80ï¸" (should be "☀️"). These all live in the
# 0x80-0xFF range; genuine Unicode (curly quotes ’ … at codepoints > 255) is
# left untouched. We decode each run latin-1 -> utf-8, dropping fragments that
# can't be recovered (truncated emoji from the scrape).
MOJIBAKE_RUN_RE = re.compile(r"[\x80-\xff]+")


def fix_mojibake(text: str) -> str:
    if text.isascii():
        return text

    def repl(m: "re.Match[str]") -> str:
        run = m.group(0)
        try:
            return run.encode("latin-1").decode("utf-8")
        except UnicodeError:
            # recover whatever decodes, drop the unrecoverable fragment
            return run.encode("latin-1", "ignore").decode("utf-8", "ignore")

    return MOJIBAKE_RUN_RE.sub(repl, text)


# --- HTML / entities ---------------------------------------------------------
HTML_TAG_RE = re.compile(r"<[^>]+>")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
ENTITIES = {
    "&nbsp;": " ", "&amp;": "&", "&lt;": "<", "&gt;": ">",
    "&quot;": '"', "&#39;": "'", "&apos;": "'", "&mdash;": "—",
    "&ndash;": "–", "&hellip;": "…",
}

# --- Exact-match boilerplate lines (compared case-insensitively, stripped) ---
EXACT_DROP = {
    # generic site chrome / navigation
    "skip to main content", "skip to main navigation", "menu", "search",
    "search courses", "search courses...", "search courses…", "home",
    "filter", "sort by", "sort by:", "clear saved table settings",
    "press ctrl+k to search", "open github menu", "expand user menu",
    "go to omscs", "collapse navigation", "view post in", "see more",
    "public", "recents", "recent reviews",
    # auth / account
    "sign up", "sign in", "log in", "login", "new to reddit?",
    "create your account and connect with a world of communities.",
    "continue with email", "continue with phone number",
    # social / engagement
    "share", "reply", "report", "award", "vote", "upvote", "downvote",
    "save", "follow", "learn more", "read more", "add review",
    # ads / promos
    "promoted", "advertisement", "ad.doubleclick.net",
    # footer section labels
    "resources", "georgia tech resources", "community", "top posts",
    "made with", "by the omscs community",
    # pagination
    "previous", "next",
    # footer social / nav links
    "github", "discord", "slack", "blog", "careers", "press", "help",
    "advertise", "developer platform", "reddit pro", "beta",
    "best of reddit", "about reddit", "about omshub", "about omscs",
    "course schedule", "schedule", "about",
    # legal / privacy footer links
    "privacy policy", "user agreement", "reddit rules",
    "your privacy choices", "accessibility", "terms of service",
    "gt login", "people also ask about", "people also ask about section",
    # known ad domains / advertisers seen in the data
    "squarespace", "homedepot.com",
}

# --- Regex boilerplate (case-insensitive, applied to stripped line) ----------
REGEX_DROP = [
    re.compile(p, re.IGNORECASE) for p in (
        r"^\d[\d,]*\s+upvotes?\s+·\s+\d[\d,]*\s+comments?$",  # 59 upvotes · 24 comments
        r"^\d[\d,]*\s+comments?$",                             # 26 comments
        r"^\d[\d,]*\s+upvotes?$",                              # 21 upvotes
        r"^\d+\s+(more\s+repl(y|ies)|more\s+comments?)$",     # 1 more reply
        r"^\d+\s*(year|yr|y|month|mo|day|d|hour|h|min|m)s?\s+ago$",  # 5mo ago
        r"^r/[A-Za-z0-9_]+$",                                  # r/OMSCS
        r"^u/[A-Za-z0-9_-]+$",                                 # u/username
        r"^•+$",                                               # bullet separators
        r"^©.*",                                               # copyright lines
        r".*all rights reserved.*",
        r"^rereddit:.*",                                       # reReddit: Top posts...
        r"^reddit,\s*inc\..*",
        r"^archived post\..*",
        r"^by continuing, you agree.*",
        r"^showing\s+\d+\s+to\s+\d+\s+of\s+\d+.*",             # pagination
        r"^courses per page$",
    )
]

# --- Trailer markers: once hit, drop the rest of the body --------------------
# These mark the start of "related posts" / footer regions that run to EOF.
TRAILER_MARKERS = (
    "new to reddit?",
    "people also ask about",
    "georgia tech resources",
)


def strip_html(text: str) -> str:
    text = HTML_COMMENT_RE.sub("", text)
    text = HTML_TAG_RE.sub("", text)
    for ent, rep in ENTITIES.items():
        text = text.replace(ent, rep)
    return text


def split_header(lines: list[str]) -> tuple[list[str], list[str]]:
    """Return (header, body). Header = leading SOURCE/URL/=== provenance block."""
    sep = None
    for i, line in enumerate(lines[:10]):
        if set(line.strip()) == {"="} and len(line.strip()) >= 10:
            sep = i
            break
    if sep is None:
        return [], lines
    return lines[: sep + 1], lines[sep + 1 :]


def source_title(header: list[str]) -> str | None:
    for line in header:
        if line.strip().lower().startswith("source:"):
            return line.split(":", 1)[1].strip()
    return None


def skip_nav_header(body: list[str], title: str | None) -> list[str]:
    """Drop a leading site-nav block by jumping to the page's real heading.

    Many scraped pages repeat the page title twice: once as the browser/page
    title (with a "| ..." suffix) and again as the on-page heading. Everything
    between is global navigation chrome. If the bare title reappears, start the
    content there.
    """
    if not title:
        return body
    for i, line in enumerate(body):
        s = line.strip()
        # The on-page heading starts with the title but, unlike the browser
        # page-title line, carries no " | Site Name" suffix.
        if i > 0 and s.startswith(title) and "|" not in s:
            return body[i:]
    return body


def is_boilerplate(line: str) -> bool:
    s = line.strip()
    if not s:
        return False  # blank handled separately
    low = s.lower()
    if low in EXACT_DROP:
        return True
    return any(rx.match(s) or rx.fullmatch(s) for rx in REGEX_DROP)


def truncate_trailer(body: list[str]) -> list[str]:
    for i, line in enumerate(body):
        if line.strip().lower() in TRAILER_MARKERS:
            return body[:i]
    return body


def collapse_blanks(lines: list[str]) -> list[str]:
    out: list[str] = []
    blank = False
    for line in lines:
        if line.strip():
            out.append(line.rstrip())
            blank = False
        elif not blank:
            out.append("")
            blank = True
    while out and not out[0]:
        out.pop(0)
    while out and not out[-1]:
        out.pop()
    return out


def clean_text(raw: str) -> str:
    lines = fix_mojibake(strip_html(raw)).splitlines()
    header, body = split_header(lines)
    body = skip_nav_header(body, source_title(header))
    body = truncate_trailer(body)
    body = [ln for ln in body if not is_boilerplate(ln)]
    cleaned = collapse_blanks(body)
    parts = []
    if header:
        parts.extend(line.rstrip() for line in header)
        parts.append("")
    parts.extend(cleaned)
    return "\n".join(parts).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="report reduction stats without writing output")
    ap.add_argument("--raw", type=Path, default=RAW_DIR)
    ap.add_argument("--out", type=Path, default=CLEAN_DIR)
    args = ap.parse_args()

    if not args.raw.is_dir():
        print(f"error: raw dir not found: {args.raw}", file=sys.stderr)
        return 1

    files = sorted(args.raw.glob("*.txt"))
    if not files:
        print(f"no .txt files in {args.raw}", file=sys.stderr)
        return 1

    if not args.check:
        args.out.mkdir(parents=True, exist_ok=True)

    for f in files:
        raw = f.read_text(encoding="utf-8", errors="replace")
        cleaned = clean_text(raw)
        before, after = len(raw.splitlines()), len(cleaned.splitlines())
        pct = (1 - after / before) * 100 if before else 0
        if args.check:
            print(f"{f.name:50s} {before:5d} -> {after:5d} lines ({pct:5.1f}% removed)")
        else:
            dest = args.out / f.name
            dest.write_text(cleaned, encoding="utf-8")
            print(f"wrote {dest.relative_to(args.out.parent.parent)}  "
                  f"({before} -> {after} lines, {pct:.1f}% removed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
