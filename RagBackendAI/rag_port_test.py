import requests
import json
import sys

# --- CONFIGURATION ---
PORT = 8001
URL = f"http://localhost:{PORT}/api/chat/"
STATUS_URL = f"http://localhost:{PORT}/api/status/"

def test_rag_connection():
    print(f"📡 Testing RAG Backend Connection on Port {PORT}...")
    print("-" * 50)

    # 1. Check if the server is even running
    try:
        status_check = requests.get(STATUS_URL, timeout=5)
        if status_check.status_code == 200:
            status = status_check.json()
            print("✅ Server: ONLINE")
            print(f"📊 RAG System Status: {'Ready' if status.get('ready') else 'Initializing'}")
            print(f"📚 Indexed Chunks: {status.get('chunks', 0)}")
        else:
            print(f"❌ Server error: {status_check.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print(f"❌ CONNECTION FAILED: Could not reach localhost:{PORT}")
        print(f"👉 Ensure you ran: python manage.py runserver {PORT}")
        return

    # 2. Test a Chat Query
    print("\n🤖 Sending test query: 'How to treat fish diseases?'")
    payload = {
        "message": "How to treat fish diseases?",
        "history": []
    }

    try:
        response = requests.post(URL, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            print("\n" + "="*20 + " AI RESPONSE " + "="*20)
            print(data.get('reply', 'No reply found'))
            print("="*53)

            if data.get('rag_results'):
                print(f"\n✅ SUCCESS: RAG retrieved {len(data['rag_results'])} pieces of evidence from your PDFs.")
            else:
                print("\n⚠️ WARNING: Response received, but no RAG context was found. Check your data folder.")
        else:
            print(f"\n❌ API Error ({response.status_code}): {response.text}")

    except Exception as e:
        print(f"\n❌ Error during chat request: {e}")

if __name__ == "__main__":
    test_rag_connection()
