import requests
import json
import sys
import os
from pathlib import Path

# --- Configuration ---
PORT = 8001
BASE_URL = f"http://localhost:{PORT}"
STATUS_URL = f"{BASE_URL}/api/status/"
CHAT_URL = f"{BASE_URL}/api/chat/"

def print_header(text):
    print("\n" + "="*60)
    print(f" {text} ".center(60, " "))
    print("="*60)

def run_diagnostic():
    print_header("🐟 KANAN BIOTECH - RAG SYSTEM TRIAL")

    # 1. Server Availability Check
    print(f"\n[1/3] Checking connectivity on port {PORT}...")
    try:
        response = requests.get(STATUS_URL, timeout=5)
        if response.status_code == 200:
            status = response.json()
            print("✅ CONNECTION: SUCCESS")
            print(f"📊 RAG READY: {status.get('ready')}")
            print(f"📚 KNOWLEDGE CHUNKS: {status.get('chunks', 0)}")
            print(f"💬 SERVER MESSAGE: {status.get('status', 'No message')}")
        else:
            print(f"❌ SERVER ERROR: Received status code {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print(f"❌ CONNECTION FAILED: Port {PORT} is not responding.")
        print(f"💡 FIX: Run 'python manage.py runserver {PORT}' first.")
        return

    # 2. Chat Connectivity & RAG Retrieval Test
    print(f"\n[2/3] Sending test query to verify AI & RAG integration...")
    test_query = "What are the ideal water parameters for tilapia farming?"
    print(f"💬 Query: \"{test_query}\"")

    payload = {
        "message": test_query,
        "history": []
    }

    try:
        start_time = requests.utils.time.time()
        chat_resp = requests.post(CHAT_URL, json=payload, timeout=45)
        elapsed = requests.utils.time.time() - start_time

        if chat_resp.status_code == 200:
            result = chat_resp.json()
            reply = result.get("reply", "")
            rag_results = result.get("rag_results", [])

            print(f"✅ CHAT API: SUCCESS (Response in {elapsed:.2f}s)")

            if rag_results:
                print(f"✅ RAG RETRIEVAL: SUCCESS ({len(rag_results)} context snippets found)")
                print(f"🔗 TOP SOURCE: {rag_results[0].get('source', 'Unknown')}")
            else:
                print("⚠️  RAG RETRIEVAL: WARNING (Response received, but NO local data was used)")
                print("   Check if your 'data/FishAquafarming/PDF' folder contains files.")

            # Preview the AI's answer
            print("\n" + "-"*20 + " AI RESPONSE PREVIEW " + "-"*20)
            preview = (reply[:200] + "...") if len(reply) > 200 else reply
            print(preview)
            print("-" * 60)
        else:
            print(f"❌ CHAT API ERROR ({chat_resp.status_code}): {chat_resp.text}")

    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")

    # 3. Final Summary
    print_header("✨ TRIAL COMPLETE")
    print("If all steps show ✅ SUCCESS, your RAG system is fully operational!")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_diagnostic()
