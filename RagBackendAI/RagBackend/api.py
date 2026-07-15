import os
import sys
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path

# Add RagSystem to path
RAG_SYSTEM_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'RagSystem')
if RAG_SYSTEM_PATH not in sys.path:
    sys.path.append(RAG_SYSTEM_PATH)

from RagSystem.rag.pipeline import RAGPipeline
from RagSystem.llm import create_client, get_response

# Global Pipeline Instance (Lazy Loading)
_pipeline = None
_client = None

def get_rag_resources():
    global _pipeline, _client
    if _pipeline is None:
        _pipeline = RAGPipeline()
        _pipeline.initialize()

    if _client is None:
        # Using os.getenv (loaded via settings.py manual loader)
        api_key = os.getenv('GROQ_API_KEY', "")
        _client = create_client(api_key)

    return _pipeline, _client

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

        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)

        pipeline, client = get_rag_resources()   #######

        if not client:
            return JsonResponse({'error': 'Groq API client not initialized. check your .env'}, status=500)

        # 1. Retrieve Context
        rag_results = pipeline.query(user_message)

        # 2. Get LLM Response
        conversation = history + [{"role": "user", "content": user_message}]

        reply, error = get_response(
            client=client,
            conversation=conversation,
            rag_results=rag_results
        )

        if error:
            return JsonResponse({'error': error}, status=500)

        return JsonResponse({
            'reply': reply,
            'rag_results': rag_results,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def get_rag_status(request):
    """Returns the status of the RAG Pipeline."""
    pipeline, _ = get_rag_resources()
    return JsonResponse({
        'ready': pipeline.is_ready(),
        'chunks': pipeline.total_chunks,
        'status': pipeline.status_msg
    })
