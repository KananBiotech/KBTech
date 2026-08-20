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
    "openai/gpt-oss-20b"       : "GPT OSS 20B — Fast ⚡",
    "openai/gpt-oss-120b"      : "GPT OSS 120B — Best Quality ⭐",
    "qwen/qwen3.6-27b"         : "Qwen 3.6 27B — Strong Quality",
}
# The former Llama models were retired by Groq and now return HTTP 404.
DEFAULT_MODEL      = "openai/gpt-oss-20b"

# ── LLM Parameters ────────────────────────────────────────────
MAX_TOKENS          = 2000
TEMPERATURE         = 0.2

# ── RAG Configuration ─────────────────────────────────────────
# Dataset Paths.  The loader scans every topic folder below DATA_ROOT, so
# FishAquafarming and any additional downloaded knowledge (such as
# BacterialLeafBlight) are indexed together.
DATA_ROOT          = RAG_BASE_DIR / "data"
DATA_DIR           = DATA_ROOT / "FishAquafarming"  # legacy cache location
PDF_DIR            = DATA_ROOT
WEB_LINKS_FILE     = DATA_ROOT

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
