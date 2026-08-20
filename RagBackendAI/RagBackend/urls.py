"""
URL configuration for RagBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .api import chat_with_rag, get_rag_status

urlpatterns = [
    path('admin/', admin.site.urls),
    # Keep the canonical slash URL, but also accept clients (such as Postman)
    # that send POST /api/chat without a trailing slash.  CommonMiddleware
    # cannot redirect a POST while preserving its body when APPEND_SLASH is
    # enabled, which otherwise turns this simple URL typo into a 500 error.
    path('api/chat', chat_with_rag, name='chat_with_rag_no_slash'),
    path('api/chat/', chat_with_rag, name='chat_with_rag'),
    path('api/status/', get_rag_status, name='get_rag_status'),
]
