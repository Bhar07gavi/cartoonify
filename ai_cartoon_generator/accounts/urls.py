"""
URL Configuration for Accounts App

Authentication routes:
- /accounts/register/ - User registration
- /accounts/login/ - User login
- /accounts/logout/ - User logout
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Registration
    path('register/', views.register, name='register'),
    
    # Login
    path('login/', views.user_login, name='login'),
    
    # Logout
    path('logout/', views.user_logout, name='logout'),
]
