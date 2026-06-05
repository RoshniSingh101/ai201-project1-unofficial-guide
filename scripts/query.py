#!/usr/bin/env python3
"""Grounded generation stage: retrieved chunks -> Groq LLM -> cited answer.

Pipeline (per the architecture diagram, the "GenAI App" box):
    user query
        -> embed_and_retrieve.retrieve(query, k)   [vector DB lookup]
        -> grounded prompt (context = retrieved chunks only)
        -> Groq llama-3.3-70b-versatile
        -> {"answer", "sources", "chunks"}

Grounding guarantees (not left to the model's goodwill):
  * The system prompt forbids using anything outside the provided documents and
    mandates the exact refusal string when the context is insufficient.
  * Source attribution is built PROGRAMMATICALLY from the retrieved chunks'
    metadata, so the cited sources are always the documents actually fed to the
    model — never invented by the LLM. When the model refuses, we return no
    sources (nothing was used).

Usage:
    python3 scripts/query.py "What are the core classes for Computer Graphics?"
    python3 scripts/query.py --test      # 2 in-domain + 1 out-of-domain query
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import embed_and_retrieve as er  # noqa: E402

MODEL = "llama-3.3-70b-versatile"
DEFAULT_K = 5  # planning.md Retrieval Approach
REFUSAL = "I don't have enough information on that."

SYSTEM_PROMPT = f"""You are an assistant that answers questions about the \
Georgia Tech OMSCS program using ONLY the reference documents provided in the \
user message.

Strict rules:
1. Use ONLY information found in the provided documents. Do not use any prior \
knowledge, training data, or outside information.
2. If the documents do not contain enough information to answer the question, \
reply with EXACTLY this sentence and nothing else: "{REFUSAL}"
3. Do not guess, infer beyond the text, or fill gaps with plausible-sounding \
information.
4. When you do answer, cite the source document name(s) in parentheses next to \
the claims they support, e.g. "(source: Specialization in Machine Learning)".
5. Be concise and list course codes/names exactly as written in the documents.
"""

USER_TEMPLATE = """Reference documents:
{context}

---
Question: {question}

Answer using only the reference documents above. If they are insufficient, \
reply exactly "{refusal}"."""


def _load_api_key() -> str | None:
    try:
        from dotenv import load_dotenv
        # look for a .env in the project root
        load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    except Exception:
        pass
    return os.getenv("GROQ_API_KEY")


def build_context(chunks: list[dict]) -> str:
    """Format retrieved chunks as numbered, source-labelled documents."""
    blocks = []
    for i, c in enumerate(chunks, 1):
        blocks.append(f"[Document {i} | source: {c['source']}]\n{c['text']}")
    return "\n\n".join(blocks)


def _unique_sources(chunks: list[dict]) -> list[str]:
    seen, out = set(), []
    for c in chunks:
        label = c["source"]
        if c.get("url"):
            label = f"{c['source']} ({c['url']})"
        if label not in seen:
            seen.add(label)
            out.append(label)
    return out


def ask(question: str, k: int = DEFAULT_K) -> dict:
    """Retrieve, generate a grounded answer, and attach programmatic sources."""
    chunks = er.retrieve(question, k)
    context = build_context(chunks)

    api_key = _load_api_key()
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY not set. Add it to a .env file in the project root "
            "(GROQ_API_KEY=...) — get a free key at https://console.groq.com."
        )

    from groq import Groq
    client = Groq(api_key=api_key)
    resp = client.chat.completions.create(
        model=MODEL,
        temperature=0,  # deterministic; minimize creative drift off-context
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_TEMPLATE.format(
                context=context, question=question, refusal=REFUSAL)},
        ],
    )
    answer = resp.choices[0].message.content.strip()

    # Programmatic attribution: if the model refused, nothing was used -> no
    # sources. Otherwise the sources ARE the retrieved documents.
    refused = REFUSAL.lower().rstrip(".") in answer.lower()
    sources = [] if refused else _unique_sources(chunks)
    return {"answer": answer, "sources": sources, "chunks": chunks}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("question", nargs="?", help="question to ask")
    ap.add_argument("-k", type=int, default=DEFAULT_K)
    ap.add_argument("--test", action="store_true",
                    help="run 2 in-domain + 1 out-of-domain grounding tests")
    ap.add_argument("--dry-run", action="store_true",
                    help="show the assembled prompt + programmatic sources "
                         "without calling the LLM (no API key needed)")
    args = ap.parse_args()

    queries = ([
        "What are the core classes for the Computer Graphics specialization?",
        "What are the elective options for Machine Learning?",
        "What's the best pizza place near the Georgia Tech campus?",  # out-of-domain
    ] if args.test else [args.question])

    for q in queries:
        if not q:
            ap.error("provide a question or use --test")
        if args.dry_run:
            chunks = er.retrieve(q, args.k)
            print("\n" + "=" * 78 + f"\nQUERY: {q}\n" + "=" * 78)
            print("SYSTEM PROMPT:\n" + SYSTEM_PROMPT)
            print("\nUSER MESSAGE:\n" + USER_TEMPLATE.format(
                context=build_context(chunks), question=q, refusal=REFUSAL)[:1500]
                  + "\n…[context truncated for display]")
            print("\nPROGRAMMATIC SOURCES (attached after generation):")
            for s in _unique_sources(chunks):
                print("  •", s)
            continue
        res = ask(q, args.k)
        print("\n" + "=" * 78 + f"\nQUERY: {q}\n" + "=" * 78)
        print("ANSWER:\n" + res["answer"])
        print("\nRETRIEVED FROM:")
        for s in res["sources"]:
            print("  •", s)
        if not res["sources"]:
            print("  (none — model reported insufficient information)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
