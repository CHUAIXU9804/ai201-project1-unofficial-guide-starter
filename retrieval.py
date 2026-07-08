"""
Milestone 4 — Embedding + vector store + retrieval.

Pipeline stages implemented here (see the Architecture diagram in planning.md):

    3a. Embedding     — encode each chunk from chunks.jsonl into a vector with
                        all-MiniLM-L6-v2 (sentence-transformers). Embeddings are
                        L2-normalized so that a cosine index behaves like a dot
                        product.
    3b. Vector Store  — persist the vectors + source metadata in ChromaDB
                        (a local, on-disk collection under chroma_db/).
    4.  Retrieval     — embed a query with the SAME model, run a cosine
                        similarity search, and return the top-k chunks with
                        their source attribution. top-k = 5 (planning.md).

The embedder used for the query is intentionally identical to the one used for
the chunks — retrieval only works if both live in the same vector space.

Usage:
    pip install -r requirements.txt
    python ingest.py                       # produces chunks.jsonl first
    python retrieval.py build              # embed chunks + build the index
    python retrieval.py query "how is the food at commons"
    python retrieval.py query "vegetarian options" --top-k 3
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# ----------------------------------------------------------------------------
# Spec (from planning.md → Retrieval Approach).
# ----------------------------------------------------------------------------
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # planning.md
DEFAULT_TOP_K = 5                                       # planning.md
CHUNKS_PATH = Path("chunks.jsonl")
CHROMA_PATH = Path("chroma_db")          # on-disk store (gitignored)
COLLECTION_NAME = "rpi_dining"

# Metadata fields we copy from each chunk into the vector store so retrieved
# results can be attributed back to their source. ChromaDB metadata values must
# be scalars (str/int/float/bool), which all of these are.
METADATA_FIELDS = ("doc_id", "source", "url", "chunk_index", "n_tokens")


# ----------------------------------------------------------------------------
# Shared: embedding model (loaded once, reused for chunks and queries)
# ----------------------------------------------------------------------------
_embedder = None


def get_embedder():
    """Load all-MiniLM-L6-v2 once and cache it for the process."""
    global _embedder
    if _embedder is None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            sys.exit("sentence-transformers is required: pip install -r requirements.txt")
        _embedder = SentenceTransformer(EMBED_MODEL)
    return _embedder


def embed_texts(texts: list[str], batch_size: int = 64):
    """Encode texts to L2-normalized vectors (returns a list of float lists)."""
    model = get_embedder()
    vectors = model.encode(
        texts,
        batch_size=batch_size,
        normalize_embeddings=True,     # unit vectors -> cosine == dot product
        show_progress_bar=len(texts) > 1,
    )
    return vectors.tolist()


def get_client():
    """A persistent (on-disk) ChromaDB client rooted at CHROMA_PATH."""
    try:
        import chromadb
    except ImportError:
        sys.exit("chromadb is required: pip install -r requirements.txt")
    return chromadb.PersistentClient(path=str(CHROMA_PATH))


# ----------------------------------------------------------------------------
# Stage 3a + 3b — Embedding + Vector Store
# ----------------------------------------------------------------------------
def load_chunks(path: Path) -> list[dict]:
    """Read the chunks.jsonl produced by ingest.py (Milestone 3)."""
    if not path.exists():
        sys.exit(f"{path} not found. Run `python ingest.py` first to produce it.")
    chunks = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not chunks:
        sys.exit(f"{path} is empty. Re-run `python ingest.py`.")
    return chunks


def build_index(chunks: list[dict], client=None) -> None:
    """
    Embed every chunk and (re)build the ChromaDB collection from scratch.

    We delete-and-recreate so a rebuild always reflects the current chunks.jsonl
    exactly, with no stale vectors left behind from a previous run.
    """
    client = client or get_client()

    # Fresh collection each build. hnsw:space=cosine matches our normalized
    # embeddings so distances are cosine distances in [0, 2].
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass  # first run: nothing to delete
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine", "embed_model": EMBED_MODEL},
    )

    print(f"Embedding {len(chunks)} chunk(s) with {EMBED_MODEL} ...")
    embeddings = embed_texts([c["text"] for c in chunks])

    ids = [c["chunk_id"] for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [{k: c.get(k, "") for k in METADATA_FIELDS} for c in chunks]

    # Add in batches to stay well under ChromaDB's per-call limits.
    BATCH = 500
    for i in range(0, len(ids), BATCH):
        sl = slice(i, i + BATCH)
        collection.add(
            ids=ids[sl],
            embeddings=embeddings[sl],
            documents=documents[sl],
            metadatas=metadatas[sl],
        )

    print(f"  stored {collection.count()} vectors -> {CHROMA_PATH}/ (collection '{COLLECTION_NAME}')")


def get_collection(client=None):
    """Open the existing collection for querying, with a helpful error if unbuilt."""
    client = client or get_client()
    try:
        return client.get_collection(COLLECTION_NAME)
    except Exception:
        sys.exit(
            f"No '{COLLECTION_NAME}' collection found in {CHROMA_PATH}/.\n"
            "Build it first:  python retrieval.py build"
        )


# ----------------------------------------------------------------------------
# Stage 4 — Retrieval
# ----------------------------------------------------------------------------
def retrieve(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    max_per_source: int | None = None,
    collection=None,
) -> list[dict]:
    """
    Embed the query with all-MiniLM-L6-v2 and return the top-k most similar
    chunks, each with its source metadata and a cosine similarity score.

    max_per_source: if set, no more than this many chunks may come from the same
        document (doc_id). This prevents one source with many near-duplicate
        chunks from monopolizing all top_k slots and crowding out a relevant
        chunk from a different source. We over-fetch candidates, then walk the
        ranked list keeping at most max_per_source per doc_id; if the cap leaves
        us short of top_k (few distinct sources matched), we backfill from the
        remaining candidates in score order. None = no cap (pure similarity).
    """
    collection = collection or get_collection()
    query_embedding = embed_texts([query])[0]

    # With a cap we need a larger candidate pool to re-select from.
    pool = top_k if max_per_source is None else min(collection.count(), max(top_k * 5, 25))
    res = collection.query(
        query_embeddings=[query_embedding],
        n_results=pool,
        include=["documents", "metadatas", "distances"],
    )

    # Chroma returns each field as a list-of-lists (one inner list per query).
    candidates: list[dict] = []
    for cid, doc, meta, dist in zip(
        res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0]
    ):
        candidates.append(
            {
                "chunk_id": cid,
                "score": 1.0 - dist,        # cosine similarity in [-1, 1]
                "distance": dist,           # cosine distance in [0, 2] (lower = closer)
                "source": meta.get("source", ""),
                "url": meta.get("url", ""),
                "doc_id": meta.get("doc_id", ""),
                "text": doc,
            }
        )

    if max_per_source is None:
        selected = candidates[:top_k]
    else:
        selected, overflow, per_source = [], [], {}
        for c in candidates:
            if per_source.get(c["doc_id"], 0) < max_per_source:
                selected.append(c)
                per_source[c["doc_id"]] = per_source.get(c["doc_id"], 0) + 1
            else:
                overflow.append(c)
            if len(selected) >= top_k:
                break
        # Backfill if the cap left us short (fewer distinct sources than top_k).
        for c in overflow:
            if len(selected) >= top_k:
                break
            selected.append(c)
        selected = selected[:top_k]

    for rank, c in enumerate(selected, start=1):
        c["rank"] = rank
    return selected


# ----------------------------------------------------------------------------
# Reporting
# ----------------------------------------------------------------------------
def print_results(query: str, results: list[dict]) -> None:
    print("\n" + "=" * 70)
    print(f"Query: {query!r}   (top {len(results)})")
    print("=" * 70)
    for r in results:
        preview = r["text"].replace("\n", " ")
        if len(preview) > 300:
            preview = preview[:300] + "…"
        print(f"\n[{r['rank']}] score={r['score']:.3f}  distance={r['distance']:.3f}  source={r['source']}  ({r['chunk_id']})")
        if r["url"]:
            print(f"    {r['url']}")
        print(f"    {preview}")


# ----------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Embed chunks, build a vector store, and retrieve (Milestone 4).")
    sub = parser.add_subparsers(dest="command", required=True)

    p_build = sub.add_parser("build", help="embed chunks.jsonl and (re)build the ChromaDB index")
    p_build.add_argument("--chunks", type=Path, default=CHUNKS_PATH)

    p_query = sub.add_parser("query", help="retrieve the top-k chunks for a query")
    p_query.add_argument("text", help="the query string")
    p_query.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    p_query.add_argument(
        "--max-per-source", type=int, default=None,
        help="cap chunks from the same document (diversity); omit for pure similarity",
    )

    args = parser.parse_args()

    if args.command == "build":
        chunks = load_chunks(args.chunks)
        build_index(chunks)
    elif args.command == "query":
        results = retrieve(args.text, top_k=args.top_k, max_per_source=args.max_per_source)
        print_results(args.text, results)


if __name__ == "__main__":
    main()
