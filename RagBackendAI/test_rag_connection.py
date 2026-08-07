import requests
import json
import sys
import time

# --- CONFIGURATION ---
# Default port for the RAG Backend
RAG_PORT = 8001
BASE_URL = f"http://localhost:{RAG_PORT}"
STATUS_URL = f"{BASE_URL}/api/status/"
CHAT_URL = f"{BASE_URL}/api/chat/"

def run_rag_trial():
    print("\n" + "="*60)
    print("🌊 KANAN BIOTECH - RAG SYSTEM CONNECTION TRIAL 🌊")
    print("="*60)

    # 1. Connectivity & Status Test
    print(f"\n[STEP 1] Testing server connectivity on port {RAG_PORT}...")
    try:
        response = requests.get(STATUS_URL, timeout=5)
        if response.status_code == 200:
            status = response.json()
            print("✅ CONNECTION SUCCESS: RAG Server is Online!")
            print(f"📊 RAG Status: {status.get('status', 'Unknown')}")
            print(f"📚 Knowledge Chunks Indexed: {status.get('chunks', 0)}")

            if not status.get('ready'):
                print("⚠️  WARNING: RAG System is still indexing. Please wait a minute and try again.")
        else:
            print(f"❌ ERROR: Server returned status code {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print(f"❌ CONNECTION FAILED: Port {RAG_PORT} is not responding.")
        print(f"👉 ACTION: Make sure you ran 'python manage.py runserver {RAG_PORT}'")
        return

    # 2. Chat & RAG Logic Test
    print(f"\n[STEP 2] Testing Chat Logic & RAG Retrieval...")
    test_query = "What is the best way to prevent bacterial infections in Tilapia?"
    print(f"💬 Query: \"{test_query}\"")

    payload = {
        "message": test_query,
        "history": []
    }

    try:
        start_time = time.time()
        print("⏳ Waiting for AI Response (this may take 10-20 seconds if RAG is searching)...")
        chat_response = requests.post(CHAT_URL, json=payload, timeout=60)
        elapsed = time.time() - start_time

        if chat_response.status_code == 200:
            result = chat_response.json()
            reply = result.get('reply', '')
            rag_results = result.get('rag_results', [])

            print(f"\n✅ CHAT SUCCESS! (Time: {elapsed:.2f}s)")
            print("\n" + "-"*20 + " AI EXPERT RESPONSE " + "-"*20)
            print(reply)
            print("-" * 60)

            if rag_results:
                print(f"📖 RAG Context: Found {len(rag_results)} document snippets.")
                print(f"🔗 Top Source: {rag_results[0].get('source', 'Local Dataset')}")
            else:
                print("⚠️  RAG NOTICE: AI responded, but NO local context was found.")
                print("   Check if your 'RagSystem/data/FishAquafarming/PDF' folder has files.")
        else:
            print(f"❌ CHAT ERROR ({chat_response.status_code}): {chat_response.text}")

    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")

    print("\n" + "="*60)
    print("✨ Trial connection test complete.")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_rag_trial()
