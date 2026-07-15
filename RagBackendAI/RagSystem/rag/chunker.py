# rag/chunker.py — Text Chunker
# ─────────────────────────────────────────────────────────────
from ..config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_pages(pages: list[dict]) -> list[dict]:
    """
    Takes the list of page dicts and splits each page's text into overlapping chunks.
    """
    chunks = []
    chunk_id = 0

    for page_data in pages:
        page_num = page_data["page"]
        text     = page_data["text"]
        source   = page_data.get("source", "Unknown")

        page_chunks = _split_text(text, CHUNK_SIZE, CHUNK_OVERLAP)

        for chunk_text in page_chunks:
            if len(chunk_text.strip()) < 30:
                continue
            chunks.append({
                "chunk_id" : chunk_id,
                "page"     : page_num,
                "text"     : chunk_text.strip(),
                "source"   : source
            })
            chunk_id += 1

    print(f"[RAG Chunker] Created {len(chunks)} chunks from {len(pages)} source items")
    return chunks

def _split_text(text: str, size: int, overlap: int) -> list[str]:
    chunks = []
    start  = 0
    while start < len(text):
        end   = start + size
        chunk = text[start:end]
        chunks.append(chunk)
        if end >= len(text):
            break
        start = end - overlap
    return chunks
