"""
Django Signals for Social Authentication

This module handles automatic user profile updates when users
sign in via Google OAuth using django-allauth.

Signals:
- pre_social_login: Fired before social account is connected
- social_account_added: Fired after social account is connected
"""

from allauth.socialaccount.signals import pre_social_login, social_account_added
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(pre_social_login)
def populate_user_profile(sender, request, sociallogin, **kwargs):
    """
    Populate user profile with data from Google OAuth
    
    This signal captures user data from Google and populates
    our custom user fields before the account is created.
    
    Args:
        sender: The sender of the signal
        request: The HTTP request
        sociallogin: The social login instance containing user data
    """
    
    # Get user data from Google
    user = sociallogin.user
    
    if sociallogin.account.provider == 'google':
        # Get extra data from Google
        extra_data = sociallogin.account.extra_data
        
        # Populate full name
        if not user.full_name:
            user.full_name = extra_data.get('name', '')
        
        # Populate profile picture
        if not user.profile_picture:
            user.profile_picture = extra_data.get('picture', '')
        
        # Auto-accept terms for social logins
        user.terms_accepted = True


@receiver(social_account_added)
def save_profile_picture(sender, request, sociallogin, **kwargs):
    """
    Save profile picture after social account is connected
    
    This ensures the profile picture is saved even if the user
    already exists in the database.
    
    Args:
        sender: The sender of the signal
        request: The HTTP request
        sociallogin: The social login instance
    """
    
    if sociallogin.account.provider == 'google':
        user = sociallogin.user
        extra_data = sociallogin.account.extra_data
        
        # Update profile picture if available
        picture_url = extra_data.get('picture', '')
        if picture_url and not user.profile_picture:
            user.profile_picture = picture_url
            user.save()
