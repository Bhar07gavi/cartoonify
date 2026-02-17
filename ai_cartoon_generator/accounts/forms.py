"""
Authentication Forms for AI Cartoon Generator

This module contains custom forms for user registration and login
with comprehensive validation and error handling.

Forms:
- UserRegistrationForm: Handles new user signup
- UserLoginForm: Handles user authentication
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """
    Custom User Registration Form
    
    Features:
    - Full name field
    - Email validation (unique)
    - Username validation (unique)
    - Strong password validation
    - Terms and conditions acceptance
    - Bootstrap styling
    """
    
    full_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name',
            'id': 'fullName'
        }),
        label='Full Name'
    )
    
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username',
            'id': 'username'
        }),
        label='Username',
        help_text='Letters, digits and @/./+/-/_ only.'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'id': 'email'
        }),
        label='Email Address'
    )
    
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a strong password',
            'id': 'password1'
        }),
        label='Password',
        help_text='Minimum 8 characters with at least one number and one special character.'
    )
    
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'id': 'password2'
        }),
        label='Confirm Password'
    )
    
    terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'terms'
        }),
        label='I agree to the Terms and Conditions',
        error_messages={
            'required': 'You must accept the terms and conditions to register.'
        }
    )
    
    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password1', 'password2']
    
    def clean_username(self):
        """Validate username is unique and meets requirements"""
        username = self.cleaned_data.get('username')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken. Please choose another.')
        
        # Check minimum length
        if len(username) < 3:
            raise ValidationError('Username must be at least 3 characters long.')
        
        return username
    
    def clean_email(self):
        """Validate email is unique"""
        email = self.cleaned_data.get('email')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise ValidationError('An account with this email already exists.')
        
        return email.lower()
    
    def clean_password1(self):
        """Validate password strength"""
        password = self.cleaned_data.get('password1')
        
        # Check minimum length
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        
        # Check for at least one number
        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one number.')
        
        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Password must contain at least one special character.')
        
        return password
    
    def clean(self):
        """Validate password confirmation matches"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match.')
        
        return cleaned_data
    
    def save(self, commit=True):
        """Save user with additional fields"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.full_name = self.cleaned_data['full_name']
        user.terms_accepted = True
        
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """
    Custom User Login Form
    
    Features:
    - Login with username or email
    - Remember me checkbox
    - Bootstrap styling
    - Custom error messages
    """
    
    username = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username or Email',
            'id': 'username',
            'autofocus': True
        }),
        label='Username or Email'
    )
    
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'password'
        }),
        label='Password'
    )
    
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'rememberMe'
        }),
        label='Remember me'
    )
    
    error_messages = {
        'invalid_login': 'Invalid username/email or password. Please try again.',
        'inactive': 'This account has been deactivated.',
    }
