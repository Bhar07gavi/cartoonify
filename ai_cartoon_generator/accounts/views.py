"""
Authentication Views for AI Cartoon Generator

This module handles all authentication-related views including:
- User registration
- User login
- User logout
- Dashboard (protected route)
- Home page

Security Features:
- CSRF protection (automatic)
- Login required decorators
- Session management
- Secure redirects
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .forms import UserRegistrationForm, UserLoginForm


def home(request):
    """
    Home page view
    
    Redirects authenticated users to dashboard,
    otherwise shows landing page.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('accounts:login')


@csrf_protect
@require_http_methods(["GET", "POST"])
def register(request):
    """
    User Registration View
    
    Handles new user signup with comprehensive validation.
    
    GET: Display registration form
    POST: Process registration and create new user
    
    Validation:
    - Username uniqueness
    - Email uniqueness
    - Password strength (8+ chars, number, special char)
    - Password confirmation match
    - Terms acceptance
    
    On Success:
    - Create user account
    - Show success message
    - Redirect to login page
    """
    
    # Redirect if already authenticated
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            # Save the new user
            user = form.save()
            
            # Success message
            messages.success(
                request,
                f'Account created successfully for {user.username}! Please login to continue.'
            )
            
            # Redirect to login page
            return redirect('accounts:login')
        else:
            # Form has validation errors
            # Errors will be displayed in the template
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
        'title': 'Sign Up - AI Cartoon Generator'
    }
    
    return render(request, 'accounts/register.html', context)


@csrf_protect
@require_http_methods(["GET", "POST"])
def user_login(request):
    """
    User Login View
    
    Handles user authentication with username or email.
    
    GET: Display login form
    POST: Authenticate user and create session
    
    Features:
    - Login with username OR email
    - Remember me functionality
    - Password visibility toggle (via JavaScript)
    - Secure session management
    
    On Success:
    - Create authenticated session
    - Redirect to dashboard or next page
    """
    
    # Redirect if already authenticated
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        
        # Get username/email from form
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        # Try to authenticate
        # First try with username
        user = authenticate(request, username=username_or_email, password=password)
        
        # If authentication failed, try with email
        if user is None:
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        
        # Check if authentication was successful
        if user is not None:
            # Log the user in
            login(request, user)
            
            # Handle "Remember Me" functionality
            if not remember_me:
                # Session expires when browser closes
                request.session.set_expiry(0)
            else:
                # Session lasts for 2 weeks (as set in settings.py)
                request.session.set_expiry(1209600)
            
            # Success message
            messages.success(
                request,
                f'Welcome back, {user.get_display_name()}!'
            )
            
            # Redirect to next page or dashboard
            next_page = request.GET.get('next', 'dashboard')
            return redirect(next_page)
        else:
            # Authentication failed
            messages.error(
                request,
                'Invalid username/email or password. Please try again.'
            )
    else:
        form = UserLoginForm()
    
    context = {
        'form': form,
        'title': 'Login - AI Cartoon Generator'
    }
    
    return render(request, 'accounts/login.html', context)


@login_required(login_url='/accounts/login/')
def user_logout(request):
    """
    User Logout View
    
    Securely logs out the user and destroys the session.
    
    Security:
    - Clears session data
    - Invalidates authentication
    - Redirects to login page
    """
    
    # Get username before logout
    username = request.user.get_display_name()
    
    # Logout the user
    logout(request)
    
    # Success message
    messages.success(
        request,
        f'You have been logged out successfully. See you soon, {username}!'
    )
    
    # Redirect to login page
    return redirect('accounts:login')


@login_required(login_url='/accounts/login/')
def dashboard(request):
    """
    Dashboard View (Protected Route)
    
    This is the main user dashboard displayed after successful login.
    
    Security:
    - Requires authentication (@login_required decorator)
    - Automatic redirect to login if not authenticated
    
    Features:
    - Welcome message with user's name
    - Profile information display
    - Upload image functionality (placeholder for future AI features)
    - Logout option
    
    Future Integration:
    - This dashboard will later include AI cartoon transformation features
    - Image upload and processing
    - Gallery of transformed images
    - User preferences
    """
    
    user = request.user
    
    context = {
        'title': 'Dashboard - AI Cartoon Generator',
        'user': user,
        'display_name': user.get_display_name(),
        'profile_picture': user.profile_picture,
        'email': user.email,
        'username': user.username,
    }
    
    return render(request, 'accounts/dashboard.html', context)
