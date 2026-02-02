from django.urls import path
from .views import login, logout, register, verify, delete_all, save_session

urlpatterns = [

    path('auth/login/', login, name='login'),
    path('auth/logout/', logout, name='logout'),
    path('auth/signup/', register, name='register'),
    path('auth/verify/', verify, name='verify'),
    path('auth/save_session/', save_session, name='verify'),

    # Dev only
    path('auth/delete_all_users', delete_all, name='delete')
]