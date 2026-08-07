import requests
import json
import sys
import time

# --- CONFIGURATION ---
PORT = 8001
BASE_URL = f"http://localhost:{PORT}"
ENDPOINTS = {
    "status": f"{BASE_URL}/api/status/",
    "chat": f"{BASE_URL}/api/chat/"
}

def log(msg, symbol="ℹ️"):
    print(f"{symbol} {msg}")

def run_test():
    print("\n" + "═"*60)
    print("🚀 KANAN BIOTECH - RAG SYSTEM PORT-WISE TRIAL TEST")
    print("═"*60)

    # 1. SERVER CONNECTIVITY CHECK
    log(f"Checking if server is running on port {PORT}...", "📡")
    try:
        response = requests.get(ENDPOINTS["status"], timeout=5)
        if response.status_code == 200:
            status_data = response.json()
            log("Server Connection: SUCCESS", "✅")
            log(f"RAG Status: {status_data.get('status', 'Unknown')}", "📊")
            log(f"Knowledge Base Chunks: {status_data.get('chunks', 0)}", "📚")
            if not status_data.get('ready'):
                log("WARNING: RAG system is still initializing. Please wait a moment.", "⚠️")
        else:
            log(f"Server returned error code {response.status_code}", "❌")
            return
    except requests.exceptions.ConnectionError:
        log(f"CONNECTION FAILED: Port {PORT} is not responding.", "❌")
        log(f"👉 ACTION REQUIRED: Run 'python manage.py runserver {PORT}' in your terminal.", "💡")
        return

    # 2. CHAT & RAG LOGIC TEST
    print("\n" + "─"*60)
    test_query = "What are the common symptoms of fish disease in aquaculture?"
    log(f"Sending Test Query: \"{test_query}\"", "🤖")

    payload = {
        "message": test_query,
        "history": []
    }

    try:
        start_time = time.time()
        chat_response = requests.post(ENDPOINTS["chat"], json=payload, timeout=60)
        elapsed = time.time() - start_time

        if chat_response.status_code == 200:
            result = chat_response.json()
            log(f"Chat Response: SUCCESS ({elapsed:.2f}s)", "✅")

            # Check RAG results
            rag_results = result.get('rag_results', [])
            if rag_results:
                log(f"RAG Retrieval: SUCCESS ({len(rag_results)} snippets found)", "✅")
                log(f"Primary Source used: {rag_results[0].get('source', 'Unknown')}", "📖")
            else:
                log("RAG Retrieval: FAILED (No local context was used for this answer)", "⚠️")
                log("👉 Check if your data/FishAquafarming/PDF folder contains your documents.", "💡")

            print("\n--- AI EXPERT REPLY PREVIEW ---")
            print(result.get('reply', 'No reply field found')[:300] + "...")
            print("-" * 31)

        else:
            log(f"Chat API Error ({chat_response.status_code}): {chat_response.text}", "❌")

    except Exception as e:
        log(f"An unexpected error occurred: {str(e)}", "❌")

    print("\n" + "═"*60)
    print("✨ TRIAL COMPLETE")
    print("═"*60 + "\n")

if __name__ == "__main__":
    run_test()
