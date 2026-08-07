import requests
import json
import sys

# Default RAG Server Port
PORT = 8001
URL = f"http://localhost:{PORT}/api/chat/"
STATUS_URL = f"http://localhost:{PORT}/api/status/"

def main():
    print("\n" + "═"*60)
    print("🐟  Kanan Biotech - RAG CHAT SIMULATOR  🐟")
    print("═"*60)
    print(f"Connecting to RAG Server on: {URL}")

    # 1. Initial Connection Check
    try:
        resp = requests.get(STATUS_URL, timeout=5)
        if resp.status_code == 200:
            status = resp.json()
            print(f"✅ STATUS: Online | Chunks: {status.get('chunks', 0)} | Ready: {status.get('ready')}")
        else:
            print(f"⚠️  STATUS: Server responded with error {resp.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: The RAG server is not running on port 8001.")
        print("👉 Please run: python manage.py runserver 8001")
        return

    print("\n[Type 'exit' to quit]")
    history = []

    while True:
        query = input("\n👤 Farmer: ").strip()

        if query.lower() in ['exit', 'quit', 'bye']:
            print("👋 Closing simulator.")
            break

        if not query:
            continue

        print("🤖 AquaBot is thinking...")

        payload = {
            "message": query,
            "history": history
        }

        try:
            response = requests.post(URL, json=payload, timeout=45)

            if response.status_code == 200:
                data = response.json()
                reply = data.get('reply', 'No reply field')
                rag_results = data.get('rag_results', [])

                # Print AI Reply
                print(f"\n🌊 AquaBot Expert:\n{reply}")

                # Print Sources (The RAG evidence)
                if rag_results:
                    print("\n📚 RAG SOURCES USED:")
                    seen_sources = set()
                    for res in rag_results:
                        source = res.get('source', 'Unknown')
                        page = res.get('page', 'N/A')
                        source_id = f"{source} (Page {page})"
                        if source_id not in seen_sources:
                            print(f"  • {source_id}")
                            seen_sources.add(source_id)
                else:
                    print("\n⚠️  No RAG sources found for this query.")

                # Add to history for context
                history.append({"role": "user", "content": query})
                history.append({"role": "assistant", "content": reply})

            else:
                print(f"\n❌ SERVER ERROR ({response.status_code}): {response.text}")

        except Exception as e:
            print(f"\n❌ REQUEST FAILED: {e}")

if __name__ == "__main__":
    main()
