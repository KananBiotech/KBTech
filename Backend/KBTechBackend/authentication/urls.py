from django.urls import path
from .views import login, logout, register, verify, delete_all, save_session
from .ai_views import ai_chat_proxy, get_seasonal_advice

urlpatterns = [

    path('auth/login/', login, name='login'),
    path('auth/logout/', logout, name='logout'),
    path('auth/signup/', register, name='register'),
    path('auth/verify/', verify, name='verify'),
    path('auth/save_session/', save_session, name='verify'),

    # AI & RAG Endpoints
    path('ai/chat/', ai_chat_proxy, name='ai_chat'),
    path('ai/seasonal-advice/', get_seasonal_advice, name='seasonal_advice'),

    # Dev only
    path('auth/delete_all_users', delete_all, name='delete')
]