import os
import requests
import json
import re
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

# Get RAG Backend URL from environment, default to localhost for dev
RAG_BACKEND_URL = os.getenv('RAG_BACKEND_URL', 'http://localhost:8001')

def get_current_season():
    month = datetime.now().month
    if 3 <= month <= 6:
        return "Summer"
    elif 7 <= month <= 10:
        return "Monsoon"
    else:
        return "Winter"

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def ai_chat_proxy(request):
    """
    Proxies chat requests from Frontend -> Main Backend -> RAG Backend
    """
    try:
        user_message = request.data.get('message')
        history = request.data.get('history', [])

        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)

        response = requests.post(
            f"{RAG_BACKEND_URL}/api/chat/",
            json={'message': user_message, 'history': history},
            timeout=30
        )

        if response.status_code != 200:
            return JsonResponse({'error': 'RAG Backend error'}, status=response.status_code)

        return JsonResponse(response.json())

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_seasonal_advice(request):
    """
    Fetches daily seasonal advice using RAG and returns structured JSON
    """
    try:
        season = get_current_season()
        # Prompting for a structured JSON response
        query = (
            f"Act as an Aquaculture expert. Based on the current {season} season, "
            "provide a list of exactly 3 common fish diseases. "
            "Return ONLY a JSON object with this exact structure: "
            "{\"diseases\": [{\"name\": \"...\", \"description\": \"...\", \"severity\": \"High/Medium/Critical\", "
            "\"symptoms\": [\"...\", \"...\"], \"prevention\": \"...\", \"product\": \"...\"}]}"
        )

        response = requests.post(
            f"{RAG_BACKEND_URL}/api/chat/",
            json={'message': query, 'history': []},
            timeout=30
        )

        if response.status_code != 200:
            return JsonResponse({'error': 'RAG Backend error'}, status=response.status_code)

        rag_data = response.json()
        reply_text = rag_data.get('reply', '')

        # Extract JSON using regex
        json_match = re.search(r'\{.*\}', reply_text, re.DOTALL)
        if json_match:
            try:
                structured_data = json.loads(json_match.group(0))
                return JsonResponse({
                    'season': season,
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    **structured_data
                })
            except json.JSONDecodeError:
                pass

        return JsonResponse({
            'season': season,
            'advice_text': reply_text,
            'error': 'Could not parse structured JSON from AI'
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
