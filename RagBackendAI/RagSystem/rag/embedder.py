# rag/embedder.py — Embedding Generator
# ─────────────────────────────────────────────────────────────
import numpy as np
from fastembed import TextEmbedding
# Use relative import to avoid conflict with 'config' package in site-packages
from ..config import EMBEDDING_MODEL

# We map the config name to fastembed supported names if needed,
# but fastembed supports "BAAI/bge-small-en-v1.5" and "sentence-transformers/all-MiniLM-L6-v2"
# Defaulting to BGE as it's often better, but honoring config.

_model = None

def get_model() -> TextEmbedding:
    global _model
    if _model is None:
        model_name = EMBEDDING_MODEL
        # Normalize name for fastembed if necessary
        if model_name == "all-MiniLM-L6-v2":
            model_name = "sentence-transformers/all-MiniLM-L6-v2"

        print(f"[RAG Embedder] Loading: {model_name}")
        _model = TextEmbedding(model_name=model_name)
        print(f"[RAG Embedder] Model ready")
    return _model

def embed_chunks(chunks: list) -> np.ndarray:
    model = get_model()
    texts = [c["text"] for c in chunks]
    print(f"[RAG Embedder] Embedding {len(texts)} chunks...")
    embeddings = np.array(list(model.embed(texts)), dtype=np.float32)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / np.maximum(norms, 1e-10)
    return embeddings

def embed_query(query: str) -> np.ndarray:
    model = get_model()
    vec   = np.array(list(model.embed([query])), dtype=np.float32)
    norm  = np.linalg.norm(vec, axis=1, keepdims=True)
    return vec / np.maximum(norm, 1e-10)
