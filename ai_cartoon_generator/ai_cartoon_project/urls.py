"""
URL configuration for ai_cartoon_project project.

This configuration includes:
- Admin panel
- Custom authentication routes
- Google OAuth routes (django-allauth)
- Dashboard route
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as account_views

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # Custom authentication URLs
    path('accounts/', include('accounts.urls')),
    
    # Django-allauth URLs (for Google OAuth)
    path('auth/', include('allauth.urls')),
    
    # Dashboard (protected route)
    path('dashboard/', account_views.dashboard, name='dashboard'),
    
    # Home page redirect
    path('', account_views.home, name='home'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
