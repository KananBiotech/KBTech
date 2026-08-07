import requests
import json
import sys

# --- SETTINGS ---
# You can change the port here if your server is running on a different one
SERVER_PORT = 8001
BASE_URL = f"http://localhost:{SERVER_PORT}"
CHAT_URL = f"{BASE_URL}/api/chat/"
STATUS_URL = f"{BASE_URL}/api/status/"

def run_trial():
    print(f"🚀 Initializing RAG Port-Wise Connection Test (Port: {SERVER_PORT})")
    print("-" * 60)

    # 1. Check Server Status
    print(f"📡 Step 1: Checking server status at {STATUS_URL}...")
    try:
        status_response = requests.get(STATUS_URL, timeout=5)
        if status_response.status_code == 200:
            status_data = status_response.json()
            print("✅ Server Status: ONLINE")
            print(f"📊 RAG Ready: {status_data.get('ready')}")
            print(f"📚 Chunks Loaded: {status_data.get('chunks')}")
        else:
            print(f"❌ Server returned error code: {status_response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Failed! Is the server running on port {SERVER_PORT}?")
        print(f"   Try running: python manage.py runserver {SERVER_PORT}")
        return

    # 2. Test Chat Connectivity
    print(f"\n💬 Step 2: Sending test query to {CHAT_URL}...")
    test_query = "How do I maintain water quality in a Tilapia pond?"
    payload = {
        "message": test_query,
        "history": []
    }

    try:
        print(f"📝 Query: \"{test_query}\"")
        response = requests.post(CHAT_URL, json=payload, timeout=30)

        if response.status_code == 200:
            result = response.json()
            reply = result.get('reply', '')
            rag_results = result.get('rag_results', [])

            print("\n" + "═" * 20 + " TEST RESULT " + "═" * 20)
            print(f"🤖 AI Response:\n{reply}\n")

            if rag_results:
                print(f"✅ RAG SUCCESS: Found {len(rag_results)} matching context snippets.")
                print(f"📖 Primary Source: {rag_results[0].get('source', 'Unknown Document')}")
            else:
                print("⚠️  RAG WARNING: AI replied but NO local context was found.")
                print("   Check if your 'data/FishAquafarming/PDF' folder has files.")
            print("═" * 53)
        else:
            print(f"❌ Chat API Error ({response.status_code}): {response.text}")

    except Exception as e:
        print(f"❌ Error during chat test: {e}")

if __name__ == "__main__":
    run_trial()
