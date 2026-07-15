# rag/loader.py — Dataset Loader
# ─────────────────────────────────────────────────────────────
import os
import pdfplumber
import pandas as pd
from ..config import EXCEL_CACHE_FILE

def load_dataset(pdf_dir: str, web_links_file: str) -> list[dict]:
    """
    Loads text from PDFs, Web links, and previously cached Q&A from Excel.
    """
    all_pages = []

    # 1. Load PDFs
    if os.path.exists(pdf_dir):
        pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdf_dir, pdf_file)
            print(f"[RAG Loader] Loading PDF: {pdf_file}")
            all_pages.extend(load_pdf(pdf_path, source_name=pdf_file))

    # 2. Load WebLinks file
    if os.path.exists(web_links_file):
        print(f"[RAG Loader] Loading WebLinks: {web_links_file}")
        with open(web_links_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if content.strip():
                all_pages.append({
                    "page": "Web",
                    "text": _clean_text(content),
                    "source": "WebLinks.txt"
                })

    # 3. Load New Data from Excel Cache (Dynamic Learning)
    if os.path.exists(EXCEL_CACHE_FILE):
        try:
            print(f"[RAG Loader] Loading learned data from {EXCEL_CACHE_FILE}")
            df = pd.read_excel(EXCEL_CACHE_FILE)
            for _, row in df.iterrows():
                # Combine Q&A as a single knowledge block
                combined_text = f"Question: {row['Question']}\nAnswer: {row['Answer']}"
                all_pages.append({
                    "page": "Interaction",
                    "text": _clean_text(combined_text),
                    "source": "User-History-Cache"
                })
        except Exception as e:
            print(f"[RAG Loader] Error loading Excel: {e}")

    return all_pages

def load_pdf(pdf_path: str, source_name: str) -> list[dict]:
    pages = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text and text.strip():
                    clean = _clean_text(text)
                    if len(clean) > 50:
                        pages.append({
                            "page": i,
                            "text": clean,
                            "source": source_name
                        })
    except Exception as e:
        print(f"[RAG Loader] Error reading PDF {pdf_path}: {e}")
    return pages

def _clean_text(text: str) -> str:
    import re
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()
