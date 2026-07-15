# rag/retriever.py — FAISS Vector Store & Search
# ─────────────────────────────────────────────────────────────
# Builds a FAISS index from chunk embeddings.
# Saves index to disk so it only needs to be built ONCE.
# On subsequent runs, loads from disk instantly.
#
# FAISS (Facebook AI Similarity Search) finds the most
# semantically similar chunks to any query in milliseconds,
# even across 10,000+ chunks.
#
# Edit this file if:
#   - You want to use a different vector DB (Chroma, Pinecone)
#   - You want to add metadata filtering
# ─────────────────────────────────────────────────────────────

import os
import pickle
import numpy as np
import faiss

# Use relative import to avoid conflict with 'config' package in site-packages
from ..config import FAISS_INDEX_FILE, CHUNKS_FILE, TOP_K_RESULTS, MIN_SIMILARITY, VECTOR_STORE_DIR


# ── Build & Save ──────────────────────────────────────────────
def build_index(chunks: list[dict], embeddings: np.ndarray) -> faiss.Index:
    """
    Builds a FAISS IndexFlatIP (inner product / cosine similarity)
    from the chunk embeddings and saves both index and chunks to disk.

    IndexFlatIP with normalized vectors = cosine similarity search.
    This is the most accurate (but not the fastest for huge datasets).
    For STG book size (~1000-3000 chunks), it's perfectly fast.
    """
    dim   = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings.astype(np.float32))

    # Save index and chunks
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
    # Ensure FAISS gets a string path, not a Path object
    faiss.write_index(index, str(FAISS_INDEX_FILE))

    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(chunks, f)

    print(f"[RAG Retriever] Index built: {index.ntotal} vectors | dim={dim}")
    print(f"[RAG Retriever] Saved to {VECTOR_STORE_DIR}/")
    return index


# ── Load from Disk ────────────────────────────────────────────
def load_index() -> tuple:
    """
    Loads the FAISS index and chunks from disk.

    Returns (index, chunks) if files exist.
    Returns (None, None) if not yet built.
    """
    if not os.path.exists(FAISS_INDEX_FILE) or not os.path.exists(CHUNKS_FILE):
        return None, None

    try:
        # Ensure FAISS gets a string path, not a Path object
        index = faiss.read_index(str(FAISS_INDEX_FILE))
        with open(CHUNKS_FILE, "rb") as f:
            chunks = pickle.load(f)
        print(f"[RAG Retriever] Loaded index: {index.ntotal} vectors")
        return index, chunks
    except Exception as e:
        print(f"[RAG Retriever] Load error: {e}")
        return None, None


def index_exists() -> bool:
    """Returns True if a pre-built index exists on disk."""
    return os.path.exists(FAISS_INDEX_FILE) and os.path.exists(CHUNKS_FILE)


# ── Search ────────────────────────────────────────────────────
def search(index: faiss.Index, chunks: list[dict],
           query_embedding: np.ndarray,
           top_k: int = TOP_K_RESULTS) -> list[dict]:
    """
    Searches the FAISS index for the top_k most similar chunks.

    Returns a list of result dicts, sorted by similarity:
        [
          {
            "chunk_id"  : 42,
            "page"      : 15,
            "text" : "For mild malaria, use Chloroquine 25mg/kg...",
            "score"     : 0.87,
          },
          ...
        ]

    Only returns chunks above MIN_SIMILARITY threshold.
    """
    if index is None or chunks is None:
        return []

    query_vec = query_embedding.astype(np.float32)

    # FAISS search — returns (scores, indices)
    scores, indices = index.search(query_vec, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:                     # FAISS returns -1 for empty slots
            continue
        if float(score) < MIN_SIMILARITY: # Filter low-relevance results
            continue

        chunk = chunks[idx].copy()
        chunk["score"] = round(float(score), 4)
        results.append(chunk)

    return results
