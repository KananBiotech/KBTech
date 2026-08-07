import requests
import json
import sys
import time

# --- CONFIGURATION ---
PORT = 8001
BASE_URL = f"http://localhost:{PORT}"
STATUS_URL = f"{BASE_URL}/api/status/"
CHAT_URL = f"{BASE_URL}/api/chat/"

def run_rag_trial():
    print("\n" + "═"*60)
    print("🐟 KANAN BIOTECH - RAG SYSTEM PORT-WISE TRIAL 🐟")
    print("═"*60)

    # 1. Connectivity Check
    print(f"\n[1/3] Testing connectivity on port {PORT}...")
    try:
        response = requests.get(STATUS_URL, timeout=5)
        if response.status_code == 200:
            status = response.json()
            print("✅ CONNECTION: SUCCESS")
            print(f"📊 RAG READY: {status.get('ready')}")
            print(f"📚 KNOWLEDGE BASE: {status.get('chunks', 0)} chunks indexed")
            print(f"💬 STATUS MSG: {status.get('status', 'No message')}")
        else:
            print(f"❌ SERVER ERROR: Received status code {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print(f"❌ CONNECTION FAILED: Port {PORT} is not responding.")
        print(f"💡 FIX: Make sure you ran 'python manage.py runserver {PORT}' in your terminal.")
        return

    # 2. RAG & AI Verification
    print(f"\n[2/3] Verifying RAG Retrieval & AI Response...")
    test_query = "What is the recommended feed rate for tilapia?"
    print(f"💬 Test Query: \"{test_query}\"")

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
            reply = result.get("reply", "")
            rag_results = result.get("rag_results", [])

            print(f"✅ CHAT API: SUCCESS ({elapsed:.2f}s)")

            if rag_results:
                print(f"✅ RAG SUCCESS: Found {len(rag_results)} relevant context snippets from your data.")
                print(f"📖 TOP SOURCE: {rag_results[0].get('source', 'Unknown')}")
            else:
                print("⚠️  RAG WARNING: Response received, but NO local data was used. Check your PDF data folder.")

            print("\n--- AI EXPERT RESPONSE PREVIEW ---")
            print(reply[:300] + "...")
            print("-" * 34)
        else:
            print(f"❌ CHAT API ERROR ({chat_resp.status_code}): {chat_resp.text}")
            return

    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        return

    # 3. Interactive Mode
    print(f"\n[3/3] System Verified. Entering Interactive Trial Mode...")
    print("(Type 'exit' to stop the test)")

    history = []
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            if not user_input or user_input.lower() in ['exit', 'quit', 'bye']:
                print("👋 Trial completed. Goodbye!")
                break

            print("🤖 AI is thinking...", end="\r")
            payload = {"message": user_input, "history": history}
            response = requests.post(CHAT_URL, json=payload, timeout=60)

            if response.status_code == 200:
                data = response.json()
                reply = data.get("reply", "")
                print(f"🤖 AI: {reply}")

                # Maintain history for conversation flow
                history.append({"role": "user", "content": user_input})
                history.append({"role": "assistant", "content": reply})
            else:
                print(f"❌ Error: {response.status_code}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    run_rag_trial()
