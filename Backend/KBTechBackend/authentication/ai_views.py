import os
import requests
import json
import re
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .mongo import get_database, mongo_error_message

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
        user_id = request.data.get('user_id')

        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)

        response = requests.post(
            f"{RAG_BACKEND_URL}/api/chat/",
            json={'message': user_message, 'history': history, 'user_id': user_id},
            timeout=30
        )

        if response.status_code != 200:
            return JsonResponse({'error': 'RAG Backend error'}, status=response.status_code)

        payload = response.json()
        if user_id:
            db = get_database()
            now = datetime.utcnow()
            db.chat_messages.insert_many([
                {'user_id': str(user_id), 'role': 'user', 'content': user_message, 'created_at': now},
                {'user_id': str(user_id), 'role': 'assistant', 'content': payload.get('reply', ''), 'created_at': now},
            ])
        return JsonResponse(payload)

    except Exception as e:
        return JsonResponse({'error': mongo_error_message(e)}, status=500)


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def chat_history(request):
    user_id = request.query_params.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'user_id is required'}, status=400)
    try:
        records = list(get_database().chat_messages.find({'user_id': str(user_id)}, {'_id': 0}).sort('created_at', 1).limit(200))
        return JsonResponse({'messages': [{**item, 'created_at': item['created_at'].isoformat()} for item in records]})
    except Exception as error:
        return JsonResponse({'error': mongo_error_message(error)}, status=500)


@csrf_exempt
@api_view(['DELETE'])
@permission_classes([AllowAny])
def clear_chat_history(request):
    user_id = request.query_params.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'user_id is required'}, status=400)
    try:
        get_database().chat_messages.delete_many({'user_id': str(user_id)})
        return JsonResponse({'status': 'cleared'})
    except Exception as error:
        return JsonResponse({'error': mongo_error_message(error)}, status=500)

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
                advice = {
                    'season': season,
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    **structured_data
                }
                get_database().seasonal_disease_advice.update_one(
                    {'date': advice['date'], 'season': season},
                    {'$set': {**advice, 'updated_at': datetime.utcnow()}},
                    upsert=True,
                )
                return JsonResponse(advice)
            except json.JSONDecodeError as e:
                # If JSON parsing fails, we can still return the raw text
                # along with an error indicating the parsing issue.
                pass # Fall through to return advice_text

        advice = {
            'season': season,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'advice_text': reply_text,
            'error': 'Could not parse structured JSON from AI. Displaying raw advice.'
        }
        get_database().seasonal_disease_advice.update_one(
            {'date': advice['date'], 'season': season},
            {'$set': {**advice, 'updated_at': datetime.utcnow()}},
            upsert=True,
        )
        return JsonResponse(advice)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
