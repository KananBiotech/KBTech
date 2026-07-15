# cache_manager.py — Excel Storage & Query Caching
# ─────────────────────────────────────────────────────────────
import os
import pandas as pd
from config import EXCEL_CACHE_FILE

def init_cache():
    """Ensures the Excel file exists with correct columns."""
    if not os.path.exists(EXCEL_CACHE_FILE):
        df = pd.DataFrame(columns=["Question", "Answer"])
        os.makedirs(os.path.dirname(EXCEL_CACHE_FILE), exist_ok=True)
        df.to_excel(EXCEL_CACHE_FILE, index=False)
        print(f"[Cache Manager] Created new cache file at {EXCEL_CACHE_FILE}")

def save_to_cache(question, answer):
    """Saves a new Q&A pair to the Excel sheet."""
    try:
        df = pd.read_excel(EXCEL_CACHE_FILE)
        # Check if question already exists to avoid duplicates
        if question.strip().lower() in df['Question'].str.strip().str.lower().values:
            return

        new_row = pd.DataFrame([{"Question": question, "Answer": answer}])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_excel(EXCEL_CACHE_FILE, index=False)
        print(f"[Cache Manager] Saved new interaction to Excel.")
    except Exception as e:
        print(f"[Cache Manager] Error saving to Excel: {e}")

def search_cache(query_text):
    """
    Searches Excel for an exact match of the question.
    Returns the answer if found, else None.
    """
    try:
        if not os.path.exists(EXCEL_CACHE_FILE):
            return None

        df = pd.read_excel(EXCEL_CACHE_FILE)
        # Exact match (case-insensitive)
        match = df[df['Question'].str.strip().str.lower() == query_text.strip().lower()]

        if not match.empty:
            return match.iloc[0]['Answer']
    except Exception as e:
        print(f"[Cache Manager] Error searching Excel: {e}")
    return None

def get_all_cached_data():
    """Returns all Q&A pairs for RAG training."""
    try:
        if os.path.exists(EXCEL_CACHE_FILE):
            return pd.read_excel(EXCEL_CACHE_FILE).to_dict('records')
    except:
        pass
    return []
