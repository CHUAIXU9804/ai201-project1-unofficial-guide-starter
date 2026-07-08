"""
Milestone 3 — Document ingestion + chunking.

Pipeline stages implemented here (see the Architecture diagram in planning.md):

    1. Document Ingestion  — load every file in documents/, strip HTML,
                             normalize whitespace *while preserving paragraph
                             breaks* (the \\n\\n boundaries our chunker relies on).
    2. Chunking            — recursive, token-based splitting with LangChain's
                             RecursiveCharacterTextSplitter, sized in the SAME
                             tokenizer that all-MiniLM-L6-v2 uses to embed, so a
                             "400-token chunk" means 400 tokens to the model too.

Output: chunks.jsonl (one JSON object per chunk, with source metadata), plus a
summary and 5 sample chunks printed to the console.

Usage:
    pip install -r requirements.txt
    python ingest.py                     # uses the spec below (150 / 25)
    python ingest.py --chunk-size 256 --overlap 50   # override from the CLI

Why local files instead of fetching URLs directly:
    Several sources in planning.md (Reddit, Facebook, and some blogs) block
    automated requests, so the reproducible approach is to save each source's
    text into documents/ once, then ingest that folder. Save a page as .txt
    (cleanest), .html, or .md. Name files with a leading number (e.g.
    "01_reddit_massive_list.txt") to auto-link them to row #1 of the Documents
    table in planning.md for richer metadata.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

# ----------------------------------------------------------------------------
# Spec (from planning.md → Chunking Strategy / Retrieval Approach).
# ----------------------------------------------------------------------------
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_CHUNK_SIZE = 150      # tokens  — planning.md says ~150 (tuned for retrieval recall)
DEFAULT_OVERLAP = 25          # tokens  — planning.md says ~25
DOCS_DIR = Path("documents")
OUTPUT_PATH = Path("chunks.jsonl")
PLANNING_PATH = Path("planning.md")

# all-MiniLM-L6-v2 truncates input at 256 tokens. Chunks larger than this get
# embedded using only their first 256 tokens — the rest never affects the
# vector. We warn (not fail) so you can still honor the spec deliberately.
MODEL_MAX_TOKENS = 256

# Separator priority for recursive splitting: prefer paragraph breaks, then
# lines, then sentences, then words. This keeps a restaurant entry / review /
# paragraph intact and only cuts finer when a piece is still too big.
SEPARATORS = ["\n\n", "\n", ". ", "? ", "! ", "; ", ", ", " ", ""]

SUPPORTED_SUFFIXES = {".txt", ".md", ".markdown", ".html", ".htm", ".pdf"}


# ----------------------------------------------------------------------------
# Stage 1 — Ingestion + cleaning
# ----------------------------------------------------------------------------
def read_file(path: Path) -> str:
    """Return plain text for one source file, dispatching on extension."""
    suffix = path.suffix.lower()

    if suffix in {".html", ".htm"}:
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            sys.exit("beautifulsoup4 is required for HTML files: pip install -r requirements.txt")
        soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
        # Drop non-content tags before extracting text.
        for tag in soup(["script", "style", "nav", "header", "footer", "noscript"]):
            tag.decompose()
        # separator="\n" keeps block-level boundaries so paragraphs survive.
        return soup.get_text(separator="\n")

    if suffix == ".pdf":
        try:
            import pdfplumber
        except ImportError:
            sys.exit("pdfplumber is required for PDF files: uncomment it in requirements.txt and pip install")
        with pdfplumber.open(path) as pdf:
            return "\n\n".join(page.extract_text() or "" for page in pdf.pages)

    # .txt / .md / .markdown
    return path.read_text(encoding="utf-8", errors="ignore")


def clean_text(text: str) -> str:
    """
    Normalize noise while PRESERVING paragraph structure.

    Our chunking strategy depends on \\n\\n boundaries, so cleaning collapses
    stray whitespace but is careful never to erase blank-line separators.
    """
    # Normalize unicode (curly quotes, accents, non-breaking spaces, etc.).
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("​", "").replace("\xa0", " ")  # zero-width, nbsp
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Trim trailing spaces on each line and collapse internal runs of spaces/tabs.
    lines = [re.sub(r"[ \t]+", " ", line).rstrip() for line in text.split("\n")]
    text = "\n".join(lines)

    # Collapse 3+ blank lines down to a single paragraph break.
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def parse_sources_from_planning(path: Path) -> dict[int, dict]:
    """
    Parse the Documents markdown table in planning.md so chunks can carry the
    real source name + URL. Keyed by the row number (col 1). Best-effort: if
    the file or table is missing we just return {} and fall back to filenames.
    """
    if not path.exists():
        return {}
    sources: dict[int, dict] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        # Table rows look like: | 1 | Reddit Post | A Massive List... | https://... |
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and cells[0].isdigit():
            n = int(cells[0])
            sources[n] = {"source": cells[1], "description": cells[2], "url": cells[3]}
    return sources


def load_documents(docs_dir: Path, planning: dict[int, dict]) -> list[dict]:
    """Load, clean, and attach metadata to every supported file in docs_dir."""
    if not docs_dir.exists():
        sys.exit(f"documents directory not found: {docs_dir.resolve()}")

    docs: list[dict] = []
    files = sorted(p for p in docs_dir.iterdir() if p.suffix.lower() in SUPPORTED_SUFFIXES)
    if not files:
        sys.exit(
            f"No documents found in {docs_dir}/. Save each source as .txt/.md/.html "
            "(name them 01_*, 02_* to match the planning.md table) and re-run."
        )

    for path in files:
        text = clean_text(read_file(path))
        if not text:
            print(f"  ! skipping empty file: {path.name}")
            continue

        # Link "07_hows_the_food.txt" -> row #7 of the planning table, if present.
        leading = re.match(r"(\d+)", path.name)
        meta = planning.get(int(leading.group(1)), {}) if leading else {}
        docs.append(
            {
                "doc_id": path.stem,
                "path": str(path),
                "source": meta.get("source", path.stem),
                "url": meta.get("url", ""),
                "text": text,
            }
        )
    return docs


# ----------------------------------------------------------------------------
# Stage 2 — Chunking
# ----------------------------------------------------------------------------
def build_splitter(chunk_size: int, overlap: int):
    """
    RecursiveCharacterTextSplitter measuring length in embedding-model tokens.

    Using the model's own tokenizer (not len() over characters) means our
    chunk_size is expressed in the exact units the embedder truncates on.
    """
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
    except ImportError:
        sys.exit("langchain-text-splitters is required: pip install -r requirements.txt")
    try:
        from transformers import AutoTokenizer
    except ImportError:
        sys.exit("transformers (installed with sentence-transformers) is required for token counting")

    tokenizer = AutoTokenizer.from_pretrained(EMBED_MODEL)
    return RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer,
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=SEPARATORS,
    ), tokenizer


def chunk_documents(docs: list[dict], splitter, tokenizer) -> list[dict]:
    """Split each document and attach per-chunk metadata."""
    chunks: list[dict] = []
    for doc in docs:
        pieces = splitter.split_text(doc["text"])
        for i, piece in enumerate(pieces):
            n_tokens = len(tokenizer.encode(piece, add_special_tokens=False))
            chunks.append(
                {
                    "chunk_id": f"{doc['doc_id']}::{i}",
                    "doc_id": doc["doc_id"],
                    "source": doc["source"],
                    "url": doc["url"],
                    "chunk_index": i,
                    "n_tokens": n_tokens,
                    "text": piece,
                }
            )
    return chunks


# ----------------------------------------------------------------------------
# Reporting
# ----------------------------------------------------------------------------
def summarize(chunks: list[dict], docs: list[dict], output_path: Path) -> None:
    print("\n" + "=" * 70)
    print(f"Ingested {len(docs)} document(s) -> {len(chunks)} chunk(s)")
    print("=" * 70)

    for doc in docs:
        n = sum(1 for c in chunks if c["doc_id"] == doc["doc_id"])
        print(f"  {doc['doc_id']:<45} {n:>4} chunks  ({doc['source']})")

    token_counts = [c["n_tokens"] for c in chunks]
    if token_counts:
        avg = sum(token_counts) / len(token_counts)
        print(
            f"\n  tokens/chunk  min={min(token_counts)}  "
            f"max={max(token_counts)}  avg={avg:.0f}"
        )
        over = sum(1 for t in token_counts if t > MODEL_MAX_TOKENS)
        if over:
            print(
                f"\n  ⚠  {over} chunk(s) exceed {EMBED_MODEL}'s {MODEL_MAX_TOKENS}-token limit.\n"
                f"     all-MiniLM-L6-v2 will embed only their first {MODEL_MAX_TOKENS} tokens;\n"
                f"     the remainder is silently dropped from the vector.\n"
                f"     Consider --chunk-size {MODEL_MAX_TOKENS} (or smaller) to match the model."
            )

    print(f"\n  wrote -> {output_path}")


def print_samples(chunks: list[dict], k: int = 5) -> None:
    """Print k spread-out sample chunks (handy for the README 'Sample Chunks' table)."""
    if not chunks:
        return
    print("\n" + "=" * 70)
    print(f"{min(k, len(chunks))} sample chunk(s)")
    print("=" * 70)
    step = max(1, len(chunks) // k)
    for c in chunks[::step][:k]:
        preview = c["text"].replace("\n", " ")
        if len(preview) > 320:
            preview = preview[:320] + "…"
        print(f"\n[{c['chunk_id']}]  source={c['source']}  tokens={c['n_tokens']}")
        print(f"  {preview}")


# ----------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Load, clean, and chunk documents (Milestone 3).")
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE, help="chunk size in tokens")
    parser.add_argument("--overlap", type=int, default=DEFAULT_OVERLAP, help="overlap in tokens")
    parser.add_argument("--docs-dir", type=Path, default=DOCS_DIR)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()

    print(f"Chunking spec: size={args.chunk_size} tokens, overlap={args.overlap} tokens")
    print(f"Tokenizer/embedder: {EMBED_MODEL}\n")

    planning = parse_sources_from_planning(PLANNING_PATH)
    docs = load_documents(args.docs_dir, planning)
    splitter, tokenizer = build_splitter(args.chunk_size, args.overlap)
    chunks = chunk_documents(docs, splitter, tokenizer)

    with args.output.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    summarize(chunks, docs, args.output)
    print_samples(chunks)


if __name__ == "__main__":
    main()
