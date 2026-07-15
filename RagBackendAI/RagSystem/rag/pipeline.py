# rag/pipeline.py — RAG Pipeline Orchestrator
# ─────────────────────────────────────────────────────────────
import os
# Use relative import to avoid conflict with 'config' package in site-packages
from ..config import PDF_DIR, WEB_LINKS_FILE, TOP_K_RESULTS

from .loader    import load_dataset
from .chunker   import chunk_pages
from .embedder  import embed_chunks, embed_query
from .retriever import build_index, load_index, index_exists, search


class RAGPipeline:
    """
    Manages the full RAG lifecycle for the FISH AQUAFARMING KNOWLEDGE knowledge base.
    """

    def __init__(self):
        self.index      = None
        self.chunks     = None
        self.ready      = False
        self.status_msg = "Not initialized"
        self.total_chunks = 0


    def initialize(self, force_rebuild=False) -> dict:
        """
        Smart initialization:
        - If vector store exists on disk and not forcing rebuild → load it
        - Otherwise → build from dataset
        """
        if not force_rebuild and index_exists():
            self.index, self.chunks = load_index()
            if self.index is not None:
                self.ready       = True
                self.total_chunks = len(self.chunks)
                self.status_msg  = f"✅ Dataset loaded — {self.total_chunks} knowledge chunks ready"
                return {
                    "success": True,
                    "message": self.status_msg,
                    "chunks" : self.total_chunks,
                    "source" : "cache",
                }

        # Build pipeline: PDF/Web -> pages-> chunks-> embeddings-> index
        try:
            print("[RAG Pipeline] Building index from dataset...")

            pages = load_dataset(PDF_DIR, WEB_LINKS_FILE)
            if not pages:
                raise ValueError(f"No data found in {PDF_DIR} or {WEB_LINKS_FILE}")

            chunks     = chunk_pages(pages)
            if not chunks:
                raise ValueError("No chunks created from dataset.")

            embeddings = embed_chunks(chunks)
            self.index = build_index(chunks, embeddings)
            self.chunks = chunks

            self.ready        = True
            self.total_chunks = len(chunks)
            self.status_msg   = (
                f"✅ Dataset indexed — {self.total_chunks} chunks from "
                f"{len(pages)} source items"
            )
            return {
                "success": True,
                "message": self.status_msg,
                "chunks" : self.total_chunks,
                "source" : "build",
            }

        except Exception as e:
            self.status_msg = f"❌ RAG build error: {str(e)}"
            return {
                "success": False,
                "message": self.status_msg,
                "chunks" : 0,
                "source" : "error",
            }


    def query(self, query_text: str, top_k: int = TOP_K_RESULTS) -> list[dict]:
        if not self.ready:
            return []

        query_vec = embed_query(query_text)
        results   = search(self.index, self.chunks, query_vec, top_k)
        return results


    def format_context(self, results: list[dict]) -> str:
        if not results:
            return ""

        lines = ["[FISH AQUAFARMING KNOWLEDGE BASE — Retrieved Evidence]"]
        lines.append("Use ONLY the following information to answer the question about FISH AQUAFARMING KNOWLEDGE.\n")

        for i, r in enumerate(results, 1):
            source_info = f"Source: {r['source']} (Page {r['page']})" if isinstance(r['page'], int) else f"Source: {r['source']}"
            lines.append(f"--- Evidence {i} ({source_info}, Relevance: {r['score']:.0%}) ---")
            lines.append(r["text"])
            lines.append("")

        lines.append("[End of Evidence]")
        return "\n".join(lines)


    def is_ready(self) -> bool:
        return self.ready
