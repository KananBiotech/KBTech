import os
from datetime import datetime, timedelta
from django.utils import timezone
from dotenv import load_dotenv
from .serializer import UserSerializer, SessionSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password

load_dotenv()

# Create your views here.
def login(request):
    try:
        return HttpResponse("Login View")
    except Exception as e:
        raise e

def logout(request):
    return HttpResponse("Logout View")

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    try:
        data = request.data  # ✅ DRF way

        print(data)

        user_data = {
            "first_name": data.get("firstName"),
            "last_name": data.get("lastName"),
            "email": data.get("email"),
            "password": make_password(data.get("password")),
            "state": data.get("state"),
            "phone": data.get("phone"),
            "farm_type": data.get("farmType"),
        }

        user_serializer = UserSerializer(data=user_data)

        print(user_serializer)

        if not user_serializer.is_valid():
            return JsonResponse(
                {"errors": user_serializer.errors},
                status=400
            )

        user = user_serializer.save()

        print('user' , user)

        session_data = {
            "user_id": user.id, # type: ignore
            "expires_at": timezone.now() + timedelta(weeks=1)
        }

        print('session_data ' , session_data)

        session_serializer = SessionSerializer(data=session_data)

        print('session serializer ', session_serializer)

        if not session_serializer.is_valid():
            return JsonResponse(
                {"errors": session_serializer.errors},
                status=400
            )

        session_serializer.save()

        return JsonResponse(
            {
                "status": 201,
                "session": session_serializer.data
            },
            status=201
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500
        )

def verify(request):
    return HttpResponse("User Info View")