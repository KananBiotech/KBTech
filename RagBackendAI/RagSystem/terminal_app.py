# terminal_app.py — CLI Rice Disease Expert
# ─────────────────────────────────────────────────────────────
import os
import sys
from dotenv import load_dotenv
from config import APP_NAME, APP_ICON, DEFAULT_MODEL
from rag.pipeline import RAGPipeline
from llm import create_client, get_response

# Load environment variables from .env file
load_dotenv()

def main():
    print(f"\n{APP_ICON} Welcome to {APP_NAME} CLI")
    print("==========================================")

    # 1. API Key Check
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("⚠️  Warning: GROQ_API_KEY not found in .env or system environment.")
        api_key = input("Please enter your Groq API Key manually: ").strip()
        if not api_key:
            print("❌ No API key provided. Exiting.")
            return

    client = create_client(api_key)
    if not client:
        print("❌ Failed to initialize Groq client. Check your API key.")
        return

    # 2. RAG Initialization
    rag = RAGPipeline()
    print("\n[1/2] Initializing Knowledge Base...")
    # Force rebuild if index doesn't exist, or just initialize
    status = rag.initialize()
    if not status["success"]:
        print(f"❌ Error: {status['message']}")
        return
    print(f"✅ Ready: {status['message']}")

    # 3. Chat Loop
    print("\n[2/2] System Ready. You can now ask about Rice Bacterial Leaf Blight.")
    print("Type 'exit' or 'quit' to stop.\n")

    conversation = []

    while True:
        try:
            user_input = input("🌾 Farmer/User: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            print("\n🔍 Searching local knowledge base...")
            results = rag.query(user_input)

            print("🤖 Expert is thinking...")
            conversation.append({"role": "user", "content": user_input})

            reply, error = get_response(
                client=client,
                conversation=conversation,
                rag_results=results,
                model=DEFAULT_MODEL
            )

            if error:
                print(f"\n❌ LLM Error: {error}")
                # Remove last user msg since we failed to get a response
                conversation.pop()
            else:
                print(f"\n🌾 Rice Expert:\n{reply}\n")
                conversation.append({"role": "assistant", "content": reply})

                # Show sources used
                if results:
                    sources = {f"{r['source']} (Page {r['page']})" if isinstance(r['page'], int) else r['source'] for r in results}
                    print(f" [📚 Sources used: {', '.join(sources)}]\n")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
