from django.urls import path
from .ai_views import ai_chat_proxy, chat_history, clear_chat_history, get_seasonal_advice

urlpatterns = [
    path('chat/', ai_chat_proxy, name='ai_chat_proxy'),
    path('chat/history/', chat_history, name='chat_history'),
    path('chat/history/clear/', clear_chat_history, name='clear_chat_history'),
    path('seasonal-advice/', get_seasonal_advice, name='get_seasonal_advice'),
]
