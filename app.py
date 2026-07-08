"""
Milestone 5 — Query interface (interactive terminal REPL).

The interface does no reasoning of its own: it reads a question, calls
generate_answer(), prints the answer, and prints the SOURCE LIST from the
code-built `result["sources"]` (derived from retrieval metadata, not from the
model). Attribution shown to the user is therefore guaranteed by the pipeline.

Run:
    python retrieval.py build                # index must exist first
    python app.py                            # starts the interactive prompt
    python app.py --top-k 3                  # optional: change how many chunks are retrieved
"""

from __future__ import annotations

import argparse

from generate import generate_answer, DEFAULT_TOP_K

BANNER = (
    "=" * 70 + "\n"
    "RPI Dining — The Unofficial Guide\n"
    "Ask about RPI's campus dining experience. Answers are grounded strictly\n"
    "in retrieved student/community sources; out-of-scope questions are refused.\n"
    "Type your question and press Enter. Type 'quit' (or Ctrl-D) to exit.\n"
    + "=" * 70
)


def render(result: dict) -> str:
    """Format the answer + source list for the terminal.

    Sources come straight from result['sources'] (built in generate.py from
    retrieval metadata). On a refusal that list is empty, so no sources print.
    """
    lines = ["", result["answer"]]
    if result["sources"]:
        lines.append("\nSources:")
        for i, s in enumerate(result["sources"], start=1):
            label = s.get("name") or s.get("source") or s.get("doc_id") or "source"
            url = s.get("url")
            lines.append(f"  [{i}] {label}" + (f" — {url}" if url else ""))
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Interactive query interface for the RPI dining guide (Milestone 5).")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K, help="chunks retrieved per question")
    args = parser.parse_args()

    print(BANNER)
    while True:
        try:
            question = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not question:
            continue
        if question.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break

        result = generate_answer(question, top_k=args.top_k)
        print(render(result))


if __name__ == "__main__":
    main()
