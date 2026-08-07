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


def get_response_with_failover(api_keys, conversation, rag_results=None, model=DEFAULT_MODEL):
    """Try configured Groq keys in order when a key is invalid or out of quota.

    The keys themselves are never logged or returned to the caller.
    """
    keys = [key.strip() for key in api_keys if key and key.strip()]
    if not keys:
        return "", "No Groq API key is configured."

    last_error = "Groq request failed."
    for index, api_key in enumerate(keys, start=1):
        client = create_client(api_key)
        reply, error = get_response(client, conversation, rag_results, model)
        if not error:
            return reply, ""

        last_error = error
        error_text = error.lower()
        # Authentication, expired/revoked keys and quota/rate-limit responses
        # are safe to retry with the next configured key.
        can_fail_over = any(marker in error_text for marker in (
            '401', '403', '429', 'authentication', 'api key', 'invalid key',
            'expired', 'revoked', 'quota', 'rate limit', 'rate_limit', 'credit',
        ))
        if not can_fail_over or index == len(keys):
            break

    return "", last_error
