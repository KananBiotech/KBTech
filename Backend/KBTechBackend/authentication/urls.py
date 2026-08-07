from django.urls import path
from .views import login, logout, register, verify, save_session

urlpatterns = [
    path('login/', login, name='login'),
    path('signup/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('verify/', verify, name='verify'),
    path('save_session/', save_session, name='save_session'),
]
