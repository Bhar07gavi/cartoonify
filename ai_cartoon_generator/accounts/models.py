"""
Custom User Model for AI Cartoon Generator

This model extends Django's AbstractUser to provide:
- Custom user fields
- Profile picture support for Google OAuth
- Full name storage
- Scalable design for future features
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom User model extending AbstractUser
    
    Fields:
    - username: inherited (unique, required)
    - email: inherited (unique, required)
    - password: inherited (hashed)
    - first_name, last_name: inherited
    - full_name: stores complete name
    - profile_picture: stores Google profile picture URL
    - created_at: timestamp of account creation
    - updated_at: timestamp of last update
    """
    
    # Additional custom fields
    full_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Full name of the user"
    )
    
    profile_picture = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="URL to user's profile picture (from Google OAuth)"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Terms acceptance
    terms_accepted = models.BooleanField(
        default=False,
        help_text="User has accepted terms and conditions"
    )
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.username
    
    def get_display_name(self):
        """Return full name if available, otherwise username"""
        return self.full_name if self.full_name else self.username
