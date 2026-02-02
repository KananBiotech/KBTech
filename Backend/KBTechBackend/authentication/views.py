from datetime import timedelta
from django.utils import timezone
from dotenv import load_dotenv
from .models import Users, Sessions
from .serializer import UserSerializer, SessionSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password, check_password

load_dotenv()

# Create your views here.
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')

        print("credentials", email, password)

        if not email or not password:
            return JsonResponse(status=404, data={
                "message": "Invalid Credentials"
            })

        existing_user = Users.objects.filter(email=email)[0]
        print("existing user is: ", existing_user.first_name)
        print(check_password(password=password, encoded=existing_user.password))
        if existing_user and check_password(password=password, encoded=existing_user.password):
            print("enterrrrrrr")
            existing_sessions = Sessions.objects.filter(user_id=existing_user.id)

            print("existing_sessions: ", existing_sessions)

            # Delete existing sessions 
            if existing_sessions:
                for session in existing_sessions:
                    session.delete() 

            session = {
                "user_id": existing_user.id,
                "expires_at": timezone.now() + timedelta(weeks=1),
                "role": existing_user.role
            }

            print(session)

            sesson_serializer = SessionSerializer(data=session)

            if not sesson_serializer.is_valid():
                return JsonResponse(
                    {"errors": sesson_serializer.errors},
                    status=400
                )
            sesson_serializer.save()

            return JsonResponse(status=201, data={
                "status": 201,
                "session": sesson_serializer.data
            })
        
        else:
            return JsonResponse(status=404, data={
                "message": "User not found"
            })

    except Exception as e:
        return JsonResponse(status=500, data={"message": "Internal Server Error"})

@csrf_exempt
@api_view(['DELETE'])
@permission_classes([AllowAny])
def logout(request):
    try:
        session = request.COOKIES.get('session')
        user_session = Sessions.objects.filter(session=session)[0]

        if not user_session:
            return JsonResponse(status=404, data={"message" : "Invalid Session"})
        
        user_session.delete()
        return JsonResponse(status=204, data={"message": "Logout Successfull"})
    except Exception as e:
        return JsonResponse(status=500, data={"message": "Internal Server Error"})

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
            "role": data.get("ROLE"),
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
            "expires_at": timezone.now() + timedelta(weeks=1),
            "role": user.role  # type: ignore
        }

        print('session_data ' , session_data)

        session_serializer = SessionSerializer(data=session_data)

        print('session serializer ', session_serializer)

        if not session_serializer.is_valid():
            return JsonResponse(
                {"errors": session_serializer.errors},
                status=400
            )

        serialised = session_serializer.save()
        print("serialised data: ", serialised)

        return JsonResponse(
            {
                "status": 201,
                "session": session_serializer.data
            },
            status=201
        )

    except Exception as e:
        return JsonResponse(status=500, data={"message": "Internal Server Error"})

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def verify(request):
    session = request.COOKIES.get('session')
    print(session)

    if not session:
        return JsonResponse(
            {"message": "session not found"},
            status=404
        )

    user_session = Sessions.objects.filter(session=session)[0]

    if user_session.expires_at < timezone.now():
        user_session.delete()
        return JsonResponse(data={
            "message": "Session Expired"
        }, status=404)

    response = {"user_id": user_session.user_id, "role": user_session.role, 'expires_at': user_session.expires_at }
    print("response = ", response)
    return JsonResponse(data=response, status=200)

@csrf_exempt
@api_view(['PUT'])
@permission_classes([AllowAny])
def save_session(request):
    
    session = request.data.get('session')
    userId = request.data.get('userId')

    if not session or not userId:
        return JsonResponse(
            {
                "status": 404,
                "message": "Parameter not found"
            }
        )

    Sessions.objects.filter(user_id=userId).update(session=session)
    return JsonResponse(
        {
            "status": 500,
            "message": "object modified"
        }
    )


# Dev Only
@csrf_exempt
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_all(request):
    # Users.objects.filter().delete()
    Sessions.objects.filter().delete()
    return HttpResponse("all users deleted.")