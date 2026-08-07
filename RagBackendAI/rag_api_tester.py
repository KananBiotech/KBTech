import requests
import json
import sys
import time

# --- CONFIGURATION ---
# Default port for the RAG Backend is 8001
RAG_PORT = 8001
BASE_URL = f"http://localhost:{RAG_PORT}"
STATUS_URL = f"{BASE_URL}/api/status/"
CHAT_URL = f"{BASE_URL}/api/chat/"

def run_diagnostic():
    print("\n" + "="*60)
    print("🚀 KANAN BIOTECH - RAG BACKEND PORT-WISE TRIAL")
    print("="*60)

    # STEP 1: Connectivity Test
    print(f"\n[1/3] Testing connectivity on port {RAG_PORT}...")
    try:
        resp = requests.get(STATUS_URL, timeout=5)
        if resp.status_code == 200:
            status_data = resp.json()
            print(f"✅ SERVER ALIVE: {BASE_URL}")
            print(f"📊 RAG READY: {status_data.get('ready')}")
            print(f"📚 KNOWLEDGE CHUNKS: {status_data.get('chunks', 0)}")
            print(f"💬 MESSAGE: {status_data.get('status', 'No status message')}")
        else:
            print(f"❌ SERVER ERROR: Status code {resp.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print(f"❌ CONNECTION FAILED: Port {RAG_PORT} is not responding.")
        print(f"👉 ACTION: Ensure you ran 'python manage.py runserver {RAG_PORT}'")
        return
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return

    # STEP 2: Chat & RAG Retrieval Test
    print(f"\n[2/3] Sending test query to verify AI + RAG integration...")
    test_query = "What are common fish diseases in aquaculture?"
    print(f"💬 Querying: \"{test_query}\"")

    payload = {
        "message": test_query,
        "history": []
    }

    try:
        start_time = time.time()
        chat_resp = requests.post(CHAT_URL, json=payload, timeout=60)
        elapsed = time.time() - start_time

        if chat_resp.status_code == 200:
            result = chat_resp.json()
            reply = result.get('reply', '')
            rag_results = result.get('rag_results', [])

            print(f"✅ CHAT SUCCESS: Received response in {elapsed:.2f}s")

            if rag_results:
                print(f"✅ RAG SUCCESS: Found {len(rag_results)} relevant document snippets.")
                print(f"📖 TOP SOURCE: {rag_results[0].get('source', 'Unknown')}")
            else:
                print("⚠️  RAG WARNING: AI replied, but NO local data chunks were found.")
                print("   Check if your 'data/FishAquafarming/PDF' folder contains files.")

            # Preview Answer
            print("\n" + "-"*20 + " AI EXPERT ANSWER " + "-"*20)
            print(reply[:300] + "..." if len(reply) > 300 else reply)
            print("-" * 58)
        else:
            print(f"❌ CHAT ERROR ({chat_resp.status_code}): {chat_resp.text}")

    except Exception as e:
        print(f"❌ REQUEST ERROR: {str(e)}")

    # STEP 3: Port Forwarding / Proxy Verification Tip
    print("\n[3/3] Stack Connectivity Tip:")
    print("If this script works, but the Main Backend (8000) or Frontend cannot reach RAG:")
    print(f"1. Check RAG_BACKEND_URL in Main Backend .env matches {BASE_URL}")
    print("2. Check Main Backend allows CORS for your Frontend domain.")

    print("\n" + "="*60)
    print("✨ Diagnostic Trial Complete.")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_diagnostic()
