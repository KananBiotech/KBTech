import uuid
from datetime import timedelta
from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from pymongo.errors import DuplicateKeyError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .mongo import get_database, mongo_error_message


def public_session(user, token=None):
    return {'user_id': str(user['_id']), 'role': user.get('role', 'user'), 'expires_at': (timezone.now() + timedelta(days=7)).isoformat(), **({'token': token} if token else {})}


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    fields = request.data
    required = {'firstName': 'first name', 'lastName': 'last name', 'email': 'email', 'password': 'password', 'phone': 'phone', 'state': 'state', 'farmType': 'farm type'}
    missing = {key: [f'{label.title()} is required.'] for key, label in required.items() if not str(fields.get(key, '')).strip()}
    if missing:
        return JsonResponse({'errors': missing}, status=400)
    try:
        db = get_database()
        user = {
            '_id': str(uuid.uuid4()), 'first_name': fields['firstName'].strip(), 'last_name': fields['lastName'].strip(),
            'email': fields['email'].strip().lower(), 'password': make_password(fields['password']),
            'phone': str(fields['phone']).strip(), 'state': fields['state'].strip(), 'farm_type': fields['farmType'].strip(),
            'role': 'user', 'created_at': timezone.now(),
        }
        db.users.insert_one(user)
        return JsonResponse({'status': 201, 'session': public_session(user)}, status=201)
    except DuplicateKeyError:
        return JsonResponse({'errors': {'email': ['An account with this email already exists.']}}, status=400)
    except Exception as error:
        return JsonResponse({'message': mongo_error_message(error)}, status=500)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email, password = request.data.get('email', '').strip().lower(), request.data.get('password', '')
    if not email or not password:
        return JsonResponse({'message': 'Email and password are required.'}, status=400)
    try:
        user = get_database().users.find_one({'email': email})
        if not user or not check_password(password, user['password']):
            return JsonResponse({'message': 'Invalid email or password.'}, status=401)
        return JsonResponse({'status': 200, 'session': public_session(user)})
    except Exception as error:
        return JsonResponse({'message': mongo_error_message(error)}, status=500)


@csrf_exempt
@api_view(['PUT'])
@permission_classes([AllowAny])
def save_session(request):
    token, user_id = request.data.get('session'), request.data.get('userId')
    if not token or not user_id:
        return JsonResponse({'message': 'Session and user ID are required.'}, status=400)
    try:
        user = get_database().users.find_one({'_id': str(user_id)}, {'role': 1})
        if not user:
            return JsonResponse({'message': 'User not found.'}, status=404)
        get_database().sessions.update_one({'user_id': str(user_id)}, {'$set': {'token': token, 'role': user.get('role', 'user'), 'expires_at': timezone.now() + timedelta(days=7)}}, upsert=True)
        return JsonResponse({'status': 200, 'message': 'Session saved.'})
    except Exception as error:
        return JsonResponse({'message': mongo_error_message(error)}, status=500)


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def verify(request):
    token = request.headers.get('Authorization', '').removeprefix('Bearer ') or request.COOKIES.get('session')
    try:
        session = get_database().sessions.find_one({'token': token, 'expires_at': {'$gt': timezone.now()}})
        if not session:
            return JsonResponse({'message': 'Invalid or expired session.'}, status=401)
        return JsonResponse({'user_id': session['user_id'], 'role': session.get('role', 'user'), 'expires_at': session['expires_at'].isoformat()})
    except Exception as error:
        return JsonResponse({'message': mongo_error_message(error)}, status=500)


@csrf_exempt
@api_view(['DELETE'])
@permission_classes([AllowAny])
def logout(request):
    token = request.headers.get('Authorization', '').removeprefix('Bearer ') or request.COOKIES.get('session')
    try:
        get_database().sessions.delete_one({'token': token})
        return JsonResponse({}, status=204)
    except Exception as error:
        return JsonResponse({'message': mongo_error_message(error)}, status=500)
