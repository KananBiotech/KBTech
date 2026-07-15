# llm.py — Groq API Client
# ─────────────────────────────────────────────────────────────
from groq import Groq
# Use relative imports to avoid conflicts with global packages
from .config import DEFAULT_MODEL, MAX_TOKENS, TEMPERATURE
from .prompt_builder import build_api_messages

def create_client(api_key: str):
    if not api_key or not api_key.strip():
        return None
    try:
        return Groq(api_key=api_key.strip())
    except Exception:
        return None

def get_response(client, conversation, rag_results=None, model=DEFAULT_MODEL):
    """
    Calls Groq API with RAG context.
    """
    if not client:
        return "", "No API client. Please provide a Groq API key."

    try:
        messages = build_api_messages(
            conversation = conversation,
            rag_results  = rag_results or [],
        )

        response = client.chat.completions.create(
            model       = model,
            max_tokens  = MAX_TOKENS,
            temperature = TEMPERATURE,
            messages    = messages,
        )
        return response.choices[0].message.content.strip(), ""

    except Exception as e:
        return "", f"API Error: {str(e)}"
