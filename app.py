#!/usr/bin/env python3
"""Gradio web UI for the OMSCS unofficial-guide RAG chatbot.

Run:
    python app.py
then open http://localhost:7860

The answer comes only from retrieved course documents, and the "Retrieved from"
panel lists the source documents the answer was grounded in.
"""
import os
import sys
from pathlib import Path

import gradio as gr

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
from query import ask  # noqa: E402


def handle_query(question: str):
    if not question or not question.strip():
        return "Please enter a question.", ""
    try:
        result = ask(question)
    except Exception as e:  # surface config errors (e.g. missing API key) in UI
        return f"Error: {e}", ""
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources or "(no sources — insufficient information)"


with gr.Blocks(title="OMSCS Unofficial Guide") as demo:
    gr.Markdown(
        "# OMSCS Unofficial Guide\n"
        "Ask about Georgia Tech OMSCS specializations, course difficulty, and "
        "workload. Answers are grounded **only** in retrieved student reviews "
        "and official specialization pages."
    )
    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g. What are the core classes for the Computer Graphics specialization?",
    )
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

    gr.Examples(
        examples=[
            "What are the elective options for Machine Learning?",
            "What are some of the hardest courses in the OMSCS program?",
            "What are the core classes for the Computer Graphics specialization?",
        ],
        inputs=inp,
    )


if __name__ == "__main__":
    # If a proxy/VPN env var routes localhost through a proxy, Gradio's
    # post-launch self-check fails ("When localhost is not accessible ...").
    # Make sure localhost bypasses any proxy.
    os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1,0.0.0.0")
    os.environ.setdefault("no_proxy", "localhost,127.0.0.1,0.0.0.0")

    # show_api=False skips Gradio's API-schema generation, which can crash with
    # "TypeError: unhashable type: 'dict'" on some gradio_client/fastapi version
    # combinations. The UI is unaffected.
    #
    # Overridable via env: set GRADIO_SHARE=1 to create a public tunnel link if
    # localhost still isn't reachable in your environment.
    demo.launch(
        show_api=False,
        server_name=os.getenv("GRADIO_SERVER_NAME", "127.0.0.1"),
        server_port=int(os.getenv("GRADIO_SERVER_PORT", "7860")),
        share=os.getenv("GRADIO_SHARE", "").lower() in ("1", "true", "yes"),
    )
