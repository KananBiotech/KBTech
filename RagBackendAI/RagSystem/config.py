# config.py — Central Configuration
import os
from pathlib import Path

# Base directory for the RagSystem
RAG_BASE_DIR = Path(__file__).resolve().parent

# ── App Info ──────────────────────────────────────────────────
APP_NAME        = "Fish Aquafarming AI"
APP_ICON        = "🐟"
APP_SUBTITLE    = "Expert Guidance on Aquaculture & Fish Farming"
APP_LAYOUT      = "wide"

# ── Sidebar ──────────────────────────────────────────────────
SIDEBAR_DEFAULT = "expanded"
STAGES = {
    "INITIAL"    : "Welcome",
    "QUESTIONING": "Analyzing Needs",
    "DIAGNOSED"  : "Expert Advice",
    "EMERGENCY"  : "Critical Intervention"
}
DIAGNOSIS_TURN_THRESHOLD = 3
CSS_FILE = "ui/style.css"

# ── Groq Models ───────────────────────────────────────────────
AVAILABLE_MODELS = {
    "llama-3.1-8b-instant"    : "Llama 3.1 8B — Requested ⚡",
    "llama-3.3-70b-versatile" : "Llama 3.3 70B — Best Quality ⭐",
    "llama3-70b-8192"         : "Llama 3 70B   — Great Quality",
    "llama3-8b-8192"          : "Llama 3 8B    — Fastest ⚡",
}
DEFAULT_MODEL      = "llama-3.1-8b-instant"

# ── LLM Parameters ────────────────────────────────────────────
MAX_TOKENS          = 2000
TEMPERATURE         = 0.2

# ── RAG Configuration ─────────────────────────────────────────
# Dataset Paths
DATA_DIR           = RAG_BASE_DIR / "data" / "FishAquafarming"
PDF_DIR            = DATA_DIR / "PDF"
WEB_LINKS_FILE     = DATA_DIR / "WebLinks.txt"

# Storage for User Queries & AI Answers
EXCEL_CACHE_FILE   = DATA_DIR / "ChatHistory_Cache.xlsx"

# Where FAISS index and chunks are saved
VECTOR_STORE_DIR   = RAG_BASE_DIR / "vector_store"
FAISS_INDEX_FILE   = VECTOR_STORE_DIR / "index.faiss"
CHUNKS_FILE        = VECTOR_STORE_DIR / "chunks.pkl"

# Embedding model
EMBEDDING_MODEL    = "all-MiniLM-L6-v2"

# Chunking settings
CHUNK_SIZE         = 1000
CHUNK_OVERLAP      = 200

# Retrieval settings
TOP_K_RESULTS      = 5
MIN_SIMILARITY     = 0.3
