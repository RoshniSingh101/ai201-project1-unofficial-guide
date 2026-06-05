#!/usr/bin/env python3
"""Embedding + retrieval stage of the RAG pipeline.

Pipeline (per the architecture diagram):
    cleaned docs -> chunk_documents.chunk_corpus()  [ingestion + chunking]
        -> SentenceTransformer("all-MiniLM-L6-v2")  [generate embeddings]
        -> ChromaDB persistent collection           [save embeddings]
        -> retrieve(query, k)                        [feeds the GenAI app]

Each chunk is stored with metadata for later attribution:
    source       – source document name (from the SOURCE: header)
    url          – original URL
    chunk_index  – position of the chunk within its source document (0-based)
    mode         – chunking strategy used (atomic / sectioned / sliding)
    tokens       – estimated token count

Usage:
    python3 scripts/embed_and_retrieve.py build          # embed + store
    python3 scripts/embed_and_retrieve.py test           # run eval queries
    python3 scripts/embed_and_retrieve.py query "..."     # ad-hoc query
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# import the ingestion/chunking stage from the sibling module
sys.path.insert(0, str(Path(__file__).resolve().parent))
import chunk_documents as cd  # noqa: E402

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION = "omscs"
CHROMA_DIR = Path(__file__).resolve().parent.parent / "documents" / "chroma"
DEFAULT_K = 8  # planning.md Retrieval Approach (raised from 5: these Reddit
               # sources carry noisy prose/comment chunks that crowd out the
               # answer-bearing table rows at k=5)

# The 3+ evaluation-plan queries used by `test`.
EVAL_QUERIES = [
    "Please give me a list of medium-level courses to take for the "
    "human-computer interaction specialization in fall/spring semesters.",
    "What are some of the hardest courses in the OMSCS program?",
    "What are the core classes for the Computer Graphics specialization?",
    "What are the elective options for Machine Learning?",
]


# --- model + store singletons (lazy so --help etc. don't import torch) -------
_model = None


def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        print(f"loading embedding model: {MODEL_NAME} ...", file=sys.stderr)
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def get_collection(reset: bool = False):
    import chromadb

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    if reset:
        try:
            client.delete_collection(COLLECTION)
        except Exception:
            pass
    # cosine space: distances land in [0, 2]; ~0 = identical, lower = closer.
    return client.get_or_create_collection(
        name=COLLECTION, metadata={"hnsw:space": "cosine"}
    )


# --- difficulty-descriptor augmentation --------------------------------------
def _is_difficulty_source(source: str) -> bool:
    return "Difficulty" in source or "Workload" in source

def _chunk_ranks(text: str) -> list[int]:
    """Ranks (first cell of each data row) appearing in a chunk, 1=easiest."""
    ranks = []
    for ln in text.splitlines():
        if cd.is_data_row(ln):
            first = ln.split("\t", 1)[0].strip().lstrip(cd._RANK_PREFIX)
            digits = "".join(ch for ch in first if ch.isdigit())
            if digits:
                ranks.append(int(digits))
    return ranks

def _difficulty_descriptor(ranks: list[int], max_rank: int) -> str:
    """A natural-language difficulty caption so table chunks (mostly course
    codes + numbers) match difficulty queries like 'hardest courses'.

    The list defines rank 1 = easiest and the max rank = hardest, but the tier
    headers (e.g. 'Tier 7 (Tell your Loved Ones goodbye)') carry no lexical
    signal for 'hard'/'easy'. We derive that signal from the rank position.
    """
    if not ranks or max_rank <= 0:
        return ""
    # The four captions are deliberately parallel — same length and sentence
    # shape — so neither extreme out-attracts the opposite query (a longer
    # "hardest" caption would also score higher on "easiest courses", breaking
    # symmetry). Each echoes the natural-language phrasing a user would use.
    frac = max(ranks) / max_rank
    if frac >= 0.8:
        return ("The hardest and most difficult courses. The toughest, "
                "highest-difficulty, heaviest-workload courses to take.")
    if frac >= 0.55:
        return ("Hard and difficult courses. Challenging, high-difficulty, "
                "high-workload courses to take.")
    if frac <= 0.25:
        return ("The easiest and simplest courses. The lightest, "
                "lowest-difficulty, lowest-workload courses to take.")
    return ("Medium and moderate courses. Average, mid-difficulty, "
            "mid-workload courses to take.")


def _embed_payload(source: str, text: str, max_rank: int) -> str:
    """The text that gets EMBEDDED for a chunk (the stored document is always
    the raw chunk text — only the retrieval vector is enriched here).

    For ranking-table chunks we prepend a difficulty descriptor derived from
    the chunk's rank position, so a tier of the hardest courses matches
    "hardest courses" even though its header ("Tier 7 (Tell your Loved Ones
    goodbye)") carries no such signal. The full text is kept (its source title
    and row tokens still carry topical signal).
    """
    if _is_difficulty_source(source):
        ranks = _chunk_ranks(text)
        if ranks:
            desc = _difficulty_descriptor(ranks, max_rank)
            return f"{source}\n\n{desc}\n\n{text}"
    return f"{source}\n\n{text}"


# --- build: embed all chunks and load them into ChromaDB ---------------------
def build() -> None:
    chunks = cd.chunk_corpus()  # hybrid chunking (the default)

    # assign each chunk its position within its own source document
    docs, metas, ids = [], [], []
    per_source_counter: dict[str, int] = {}
    for gi, c in enumerate(chunks):
        idx = per_source_counter.get(c.source, 0)
        per_source_counter[c.source] = idx + 1
        docs.append(c.text)
        metas.append({
            "source": c.source,
            "url": c.url,
            "chunk_index": idx,
            "mode": cd.doc_mode(c.source, c.url),
            "tokens": c.tokens,
        })
        # ChromaDB ids must be unique strings. The slug is truncated, so prefix
        # a global counter to stay unique even when two sources share a prefix
        # (e.g. "<spec> ... (Spring/Fall)" vs "... (Summer)").
        slug = "".join(ch if ch.isalnum() else "_" for ch in c.source)[:40]
        ids.append(f"{gi}-{slug}-{idx}")

    model = get_model()
    # Per difficulty/workload source, the max rank present = the "hardest"
    # anchor, so a chunk's rank position can be turned into a difficulty word.
    src_max_rank: dict[str, int] = {}
    for m, d in zip(metas, docs):
        if _is_difficulty_source(m["source"]):
            r = _chunk_ranks(d)
            if r:
                src_max_rank[m["source"]] = max(src_max_rank.get(m["source"], 0),
                                                max(r))

    # Context augmentation (see _embed_payload): the stored document stays the
    # raw chunk text; only the embedded vector is enriched, with ranking-table
    # chunks reduced to a concentrated difficulty summary.
    payloads = [_embed_payload(m["source"], d, src_max_rank.get(m["source"], 0))
                for m, d in zip(metas, docs)]
    embeddings = model.encode(
        payloads, show_progress_bar=True, normalize_embeddings=True
    ).tolist()

    col = get_collection(reset=True)
    col.add(documents=docs, embeddings=embeddings, metadatas=metas, ids=ids)
    print(f"stored {col.count()} chunks in ChromaDB at {CHROMA_DIR}")


# --- retrieval ---------------------------------------------------------------
def retrieve(query: str, k: int = DEFAULT_K) -> list[dict]:
    """Return the top-k most relevant chunks with their source info + distance."""
    model = get_model()
    q_emb = model.encode([query], normalize_embeddings=True).tolist()
    col = get_collection()
    res = col.query(
        query_embeddings=q_emb,
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    out = []
    for doc, meta, dist in zip(
        res["documents"][0], res["metadatas"][0], res["distances"][0]
    ):
        out.append({
            "text": doc,
            "source": meta["source"],
            "url": meta["url"],
            "chunk_index": meta["chunk_index"],
            "distance": dist,
        })
    return out


def _print_hits(query: str, hits: list[dict], preview: int = 500) -> None:
    print("\n" + "=" * 78)
    print(f"QUERY: {query}")
    print("=" * 78)
    for rank, h in enumerate(hits, 1):
        print(f"\n[{rank}] distance={h['distance']:.3f}  "
              f"source={h['source']!r}  chunk_index={h['chunk_index']}")
        text = h["text"]
        print("-" * 60)
        print(text if len(text) <= preview else text[:preview] + " …[truncated]")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build", help="embed all chunks and store in ChromaDB")
    t = sub.add_parser("test", help="run the evaluation-plan queries")
    t.add_argument("-k", type=int, default=DEFAULT_K)
    q = sub.add_parser("query", help="run an ad-hoc query")
    q.add_argument("text")
    q.add_argument("-k", type=int, default=DEFAULT_K)
    args = ap.parse_args()

    if args.cmd == "build":
        build()
    elif args.cmd == "query":
        _print_hits(args.text, retrieve(args.text, args.k))
    elif args.cmd == "test":
        for query in EVAL_QUERIES:
            _print_hits(query, retrieve(query, args.k))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
