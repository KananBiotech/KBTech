import os
import sys
import json
from datetime import datetime, timezone
from functools import lru_cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path
from pymongo import MongoClient

# Add RagSystem to path
RAG_SYSTEM_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'RagSystem')
if RAG_SYSTEM_PATH not in sys.path:
    sys.path.append(RAG_SYSTEM_PATH)

from RagSystem.rag.pipeline import RAGPipeline
from RagSystem.llm import get_response_with_failover

# Global Pipeline Instance (Lazy Loading)
_pipeline = None


def health_check(request):
    """Small, dependency-free endpoint for Render's health checks."""
    return JsonResponse({'status': 'ok'})


@lru_cache(maxsize=1)
def get_mongo_database():
    uri = os.getenv('MONGODB_URI') or os.getenv('MONGO_URI') or os.getenv('MongoURI')
    if not uri:
        return None
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    database = client.get_default_database(default=os.getenv('MONGODB_DB_NAME', 'kbtech'))
    database.ai_requests.create_index([('user_id', 1), ('created_at', -1)])
    return database

def get_rag_resources():
    global _pipeline
    if _pipeline is None:
        _pipeline = RAGPipeline()
        _pipeline.initialize()

    return _pipeline


def configured_groq_keys():
    """Return up to five keys in priority order, without exposing them."""
    first_key = os.getenv('GROQ_API_KEY_1') or os.getenv('GROQ_API_KEY')
    return [first_key, *(os.getenv(f'GROQ_API_KEY_{number}') for number in range(2, 6))]

@csrf_exempt
def chat_with_rag(request):
    """
    Endpoint for RAG-powered chat.
    Expects POST JSON: { "message": "...", "history": [] }
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get('message')
        history = data.get('history', []) # List of {"role": "user/assistant", "content": "..."}
        user_id = data.get('user_id')

        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)

        pipeline = get_rag_resources()
        api_keys = configured_groq_keys()
        if not any(api_keys):
            return JsonResponse({'error': 'Groq API client not initialized. check your .env'}, status=500)

        # 1. Retrieve Context
        rag_results = pipeline.query(user_message)

        # 2. Get LLM Response
        conversation = history + [{"role": "user", "content": user_message}]

        reply, error = get_response_with_failover(
            api_keys=api_keys,
            conversation=conversation,
            rag_results=rag_results
        )

        if error:
            return JsonResponse({'error': error}, status=500)

        # Keep a compact audit record for every authenticated RAG request.
        # Full chat messages are stored by the main Backend service.
        if user_id:
            try:
                database = get_mongo_database()
                if database is not None:
                    database.ai_requests.insert_one({
                        'user_id': str(user_id), 'question': user_message,
                        'response': reply, 'created_at': datetime.now(timezone.utc),
                    })
            except Exception:
                # Logging must never prevent the user from receiving AI advice.
                pass

        return JsonResponse({
            'reply': reply,
            'rag_results': rag_results,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def get_rag_status(request):
    """Returns the status of the RAG Pipeline."""
    pipeline = get_rag_resources()
    return JsonResponse({
        'ready': pipeline.is_ready(),
        'chunks': pipeline.total_chunks,
        'status': pipeline.status_msg
    })
