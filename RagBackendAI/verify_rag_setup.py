import os
import sys
import requests
import json
import time
from pathlib import Path
from dotenv import load_dotenv

# --- CONFIGURATION ---
PORT = 8001
BASE_URL = f"http://localhost:{PORT}"
STATUS_URL = f"{BASE_URL}/api/status/"
CHAT_URL = f"{BASE_URL}/api/chat/"

# Add RagSystem to path for library-mode testing
BASE_DIR = Path(__file__).resolve().parent
RAG_SYSTEM_PATH = str(BASE_DIR / "RagSystem")
if RAG_SYSTEM_PATH not in sys.path:
    sys.path.append(RAG_SYSTEM_PATH)

def print_box(text, color="white"):
    print("\n" + "="*70)
    print(f" {text} ".center(70, " "))
    print("="*70)

def test_server_mode():
    print(f"\n📡 [MODE 1] Testing Server Connectivity (Port {PORT})...")
    try:
        # 1. Check Status
        status_resp = requests.get(STATUS_URL, timeout=5)
        if status_resp.status_code == 200:
            status = status_resp.json()
            print(f"✅ SERVER IS ONLINE")
            print(f"📊 RAG Ready: {status.get('ready')}")
            print(f"📚 Indexed Chunks: {status.get('chunks', 0)}")

            # 2. Test Chat
            print("\n🤖 Sending test query to API...")
            payload = {"message": "Tell me about fish diseases.", "history": []}
            chat_resp = requests.post(CHAT_URL, json=payload, timeout=45)

            if chat_resp.status_code == 200:
                data = chat_resp.json()
                print("✅ CHAT SUCCESS!")
                print(f"💬 Preview: {data.get('reply', '')[:150]}...")
                if data.get('rag_results'):
                    print(f"📖 Context found in documents: YES ({len(data['rag_results'])} snippets)")
                return True
            else:
                print(f"❌ CHAT FAILED: {chat_resp.status_code} - {chat_resp.text}")
        else:
            print(f"⚠️ SERVER ERROR: Status code {status_resp.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"❌ CONNECTION FAILED: Port {PORT} is not responding.")
        print(f"👉 Start the server first: python manage.py runserver {PORT}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    return False

def test_internal_mode():
    print(f"\n🛠️ [MODE 2] Testing Internal RAG Pipeline Logic (Direct Import)...")
    load_dotenv()
    if not os.getenv("GROQ_API_KEY"):
        print("❌ ERROR: GROQ_API_KEY missing in .env")
        return False

    try:
        from RagSystem.rag.pipeline import RAGPipeline
        pipeline = RAGPipeline()
        print("⏳ Initializing Knowledge Base (this may take a few seconds)...")
        init = pipeline.initialize()

        if init.get("success"):
            print(f"✅ PIPELINE READY: {init.get('message')}")
            print(f"📚 Chunks: {init.get('chunks')}")
            # Search test
            results = pipeline.query("disease")
            print(f"🔍 Retrieval Test: Found {len(results)} snippets.")
            return True
        else:
            print(f"❌ PIPELINE INIT FAILED: {init.get('message')}")
    except Exception as e:
        print(f"❌ INTERNAL ERROR: {e}")
        import traceback
        traceback.print_exc()
    return False

if __name__ == "__main__":
    print_box("🐟 KANAN BIOTECH - RAG SYSTEM HEALTH CHECK")

    # Try server mode first
    server_ok = test_server_mode()

    # Always try internal mode to verify data indexing
    internal_ok = test_internal_mode()

    print_box("TRIAL SUMMARY")
    if server_ok and internal_ok:
        print("✅ EVERYTHING IS WORKING PERFECTLY!")
        print(f"The RAG system is reachable on port {PORT} and correctly indexing your data.")
    elif internal_ok:
        print("⚠️  INTERNAL LOGIC IS OK, BUT SERVER IS OFFLINE.")
        print(f"Run 'python manage.py runserver {PORT}' to enable the API.")
    else:
        print("❌ SYSTEM ERRORS DETECTED.")
        print("Check your .env file, PDF data folder, and dependencies in requirements.txt.")
    print("="*70 + "\n")
