"""
Tests for Accounts App

This module contains test cases for:
- User registration
- User login
- User logout
- Dashboard access
- Form validation
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationTests(TestCase):
    """Test cases for user registration"""
    
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')
    
    def test_registration_page_loads(self):
        """Test that registration page loads successfully"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
    
    def test_valid_registration(self):
        """Test registration with valid data"""
        data = {
            'full_name': 'Test User',
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
            'terms': True
        }
        response = self.client.post(self.register_url, data)
        
        # Check user was created
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
    
    def test_duplicate_username(self):
        """Test registration with existing username"""
        User.objects.create_user(
            username='testuser',
            email='existing@example.com',
            password='TestPass123!'
        )
        
        data = {
            'full_name': 'New User',
            'username': 'testuser',
            'email': 'new@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
            'terms': True
        }
        response = self.client.post(self.register_url, data)
        
        # Should still have only one user
        self.assertEqual(User.objects.count(), 1)


class UserLoginTests(TestCase):
    """Test cases for user login"""
    
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
    
    def test_login_page_loads(self):
        """Test that login page loads successfully"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_valid_login(self):
        """Test login with valid credentials"""
        data = {
            'username': 'testuser',
            'password': 'TestPass123!'
        }
        response = self.client.post(self.login_url, data)
        
        # Check user is authenticated
        self.assertTrue(response.wsgi_request.user.is_authenticated)


class DashboardTests(TestCase):
    """Test cases for dashboard"""
    
    def setUp(self):
        self.client = Client()
        self.dashboard_url = reverse('dashboard')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
    
    def test_dashboard_requires_login(self):
        """Test that dashboard redirects to login if not authenticated"""
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_dashboard_accessible_when_logged_in(self):
        """Test that dashboard is accessible for authenticated users"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')
