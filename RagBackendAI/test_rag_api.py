import requests
import json
import time
import sys

# Configuration - Change port if you are running on a different one
PORT = 8001
BASE_URL = f"http://localhost:{PORT}"
CHAT_ENDPOINT = f"{BASE_URL}/api/chat/"
STATUS_ENDPOINT = f"{BASE_URL}/api/status/"

def test_connection():
    print(f"🔍 Testing RAG Backend connectivity on port {PORT}...")

    # 1. Check if server is alive and get RAG status
    try:
        print(f"📡 Pinging Status Endpoint: {STATUS_ENDPOINT}")
        status_resp = requests.get(STATUS_ENDPOINT, timeout=10)
        if status_resp.status_code == 200:
            data = status_resp.json()
            print("✅ Server is ALIVE!")
            print(f"📊 RAG Status: {'READY' if data.get('ready') else 'INITIALIZING'}")
            print(f"📚 Knowledge Chunks: {data.get('chunks', 0)}")
            print(f"💬 Message: {data.get('status', 'No status message')}")
        else:
            print(f"⚠️ Server returned status code: {status_resp.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"❌ ERROR: Could not connect to port {PORT}.")
        print(f"👉 Make sure you ran: python manage.py runserver {PORT}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error during ping: {e}")
        return False

    print("\n" + "="*50)

    # 2. Test Chat Connection
    print("🤖 Sending Test Chat Query to AI...")
    test_payload = {
        "message": "What is the ideal water temperature for Tilapia farming?",
        "history": []
    }

    try:
        start_time = time.time()
        print(f"📤 POST {CHAT_ENDPOINT}")
        # Note: First request might take longer if the RAG pipeline is initializing
        response = requests.post(CHAT_ENDPOINT, json=test_payload, timeout=60)
        elapsed = time.time() - start_time

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response received in {elapsed:.2f} seconds!")
            print("\n--- AI EXPERT REPLY ---")
            print(result.get('reply', 'No reply field in response'))
            print("-" * 25)

            # Verify RAG Results
            rag_results = result.get('rag_results', [])
            if rag_results:
                print(f"🔍 RAG successfully retrieved {len(rag_results)} context snippets.")
                print(f"📖 Top Source: {rag_results[0].get('source', 'Unknown')}")
            else:
                print("⚠️ Warning: AI replied, but NO RAG results were found. Check if your PDF/Web data is loaded.")
        else:
            print(f"❌ Chat Error (Status {response.status_code}): {response.text}")

    except Exception as e:
        print(f"❌ Failed to complete chat test: {e}")

    return True

if __name__ == "__main__":
    if not test_connection():
        sys.exit(1)
    print("\n✨ Trial complete.")
