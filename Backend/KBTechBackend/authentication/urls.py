from django.urls import path
from .views import login, logout, register, verify

urlpatterns = [

    path('auth/login/', login, name='login'),
    path('auth/logout/', logout, name='logout'),
    path('auth/signup/', register, name='register'),
    path('auth/verify/', verify, name='verify'),
]