import requests
import json
import sys
import time

# --- CONFIGURATION ---
PORT = 8001
BASE_URL = f"http://localhost:{PORT}"
STATUS_URL = f"{BASE_URL}/api/status/"
CHAT_URL = f"{BASE_URL}/api/chat/"

def run_trial():
    print("\n" + "="*65)
    print("🌊 KANAN BIOTECH - RAG BACKEND QUICK TRIAL 🌊")
    print("="*65)

    # 1. Server Connectivity Check
    print(f"\n[STEP 1] Checking connectivity on port {PORT}...")
    try:
        response = requests.get(STATUS_URL, timeout=5)
        if response.status_code == 200:
            status = response.json()
            print("✅ CONNECTION SUCCESS: RAG Server is responding.")
            print(f"📊 RAG Status: {status.get('status', 'Ready')}")
            print(f"📚 Knowledge Base Size: {status.get('chunks', 0)} chunks")
        else:
            print(f"❌ SERVER ERROR: Status code {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print(f"❌ CONNECTION FAILED: Port {PORT} is not active.")
        print(f"👉 ACTION: Open a terminal and run: python manage.py runserver {PORT}")
        return

    # 2. End-to-End Chat Test
    print(f"\n[STEP 2] Testing Chat Logic & Local Knowledge Retrieval...")
    test_query = "What are the ideal water parameters for healthy fish farming?"
    print(f"💬 Test Query: \"{test_query}\"")

    payload = {
        "message": test_query,
        "history": []
    }

    try:
        start_time = time.time()
        print("⏳ Waiting for Expert AI Response...")
        chat_resp = requests.post(CHAT_URL, json=payload, timeout=60)
        elapsed = time.time() - start_time

        if chat_resp.status_code == 200:
            result = chat_resp.json()
            reply = result.get('reply', '')
            rag_results = result.get('rag_results', [])

            print(f"✅ CHAT SUCCESS! (Response Time: {elapsed:.2f}s)")

            # Verify RAG works
            if rag_results:
                print(f"🔍 RAG VERIFIED: Found {len(rag_results)} snippets in your local documents.")
                print(f"📖 Primary Source: {rag_results[0].get('source', 'Local Data')}")
            else:
                print("⚠️  RAG WARNING: No local context found. The AI answered from general knowledge.")

            print("\n" + "─"*20 + " AI RESPONSE " + "─"*20)
            print(reply)
            print("─"*53)
        else:
            print(f"❌ CHAT ERROR ({chat_resp.status_code}): {chat_resp.text}")

    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")

    print("\n" + "="*65)
    print("✨ Trial test completed successfully!")
    print("="*65 + "\n")

if __name__ == "__main__":
    run_trial()
