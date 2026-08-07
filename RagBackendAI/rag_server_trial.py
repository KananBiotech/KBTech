import os
import sys
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

# --- CONFIGURATION ---
PORT = 8001
BASE_URL = f"http://localhost:{PORT}"
CHAT_ENDPOINT = f"{BASE_URL}/api/chat/"
STATUS_ENDPOINT = f"{BASE_URL}/api/status/"

# Add RagSystem to path for internal testing
BASE_DIR = Path(__file__).resolve().parent
RAG_SYSTEM_PATH = str(BASE_DIR / "RagSystem")
if RAG_SYSTEM_PATH not in sys.path:
    sys.path.append(RAG_SYSTEM_PATH)

def run_diagnostic():
    print("📋 STARTING RAG SYSTEM DIAGNOSTIC TRIAL...")
    print("=" * 60)

    # STEP 1: Check Environment
    print("\n[STEP 1] Checking Environment Variables...")
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        print(f"✅ GROQ_API_KEY found (starts with: {api_key[:6]}...)")
    else:
        print("❌ ERROR: GROQ_API_KEY not found in .env file.")

    # STEP 2: Internal Logic Test (Independent of Port)
    print("\n[STEP 2] Testing Internal RAG Pipeline Logic...")
    try:
        from RagSystem.rag.pipeline import RAGPipeline
        pipeline = RAGPipeline()
        init_status = pipeline.initialize()
        if init_status.get("success"):
            print(f"✅ RAG Pipeline initialized. Chunks found: {pipeline.total_chunks}")
            # Quick query test
            results = pipeline.query("fish disease")
            print(f"✅ Local Search Test: Found {len(results)} context snippets.")
        else:
            print(f"❌ RAG Initialization failed: {init_status.get('message')}")
    except Exception as e:
        print(f"❌ Internal RAG Error: {e}")

    # STEP 3: Port Connectivity Test (Requires Server Running)
    print(f"\n[STEP 3] Testing API Connectivity (Port {PORT})...")
    print(f"💡 Tip: Ensure 'python manage.py runserver {PORT}' is running.")

    try:
        # Check Status
        status_resp = requests.get(STATUS_ENDPOINT, timeout=5)
        if status_resp.status_code == 200:
            print(f"✅ Server is REACHABLE on port {PORT}.")

            # Send Test Chat
            print("🤖 Sending test chat request to API...")
            chat_payload = {
                "message": "Hello AquaBot, are you connected correctly?",
                "history": []
            }
            chat_resp = requests.post(CHAT_ENDPOINT, json=chat_payload, timeout=30)

            if chat_resp.status_code == 200:
                print("✅ API CHAT SUCCESS!")
                reply = chat_resp.json().get('reply', '')
                print(f"\nAI Response Preview: \"{reply[:100]}...\"")
            else:
                print(f"❌ API Error ({chat_resp.status_code}): {chat_resp.text}")
        else:
            print(f"⚠️ Server responded with status {status_resp.status_code}")

    except requests.exceptions.ConnectionError:
        print(f"❌ CONNECTION FAILED: Port {PORT} is not accepting connections.")
        print(f"👉 Please start the server first: python manage.py runserver {PORT}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

    print("\n" + "=" * 60)
    print("✨ Diagnostic Trial Complete.")

if __name__ == "__main__":
    run_diagnostic()
