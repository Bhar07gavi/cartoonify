# 🎨 AI Cartoon Generator - Authentication System

A production-ready authentication system built with Django, PostgreSQL, and Google OAuth for the AI-Based Image Transformation Tool for Cartoon Effect Generation.

[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Database Setup](#-database-setup)
- [Running the Application](#-running-the-application)
- [Google OAuth Setup](#-google-oauth-setup)
- [Usage](#-usage)
- [Testing](#-testing)
- [Security Features](#-security-features)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Authentication
- ✅ User Registration with validation
- ✅ User Login (username or email)
- ✅ Google OAuth Sign-In
- ✅ Remember Me functionality
- ✅ Secure Logout
- ✅ Password visibility toggle

### Security
- ✅ CSRF Protection
- ✅ Password hashing (Django's built-in)
- ✅ Strong password validation (8+ chars, number, special char)
- ✅ Login required decorators
- ✅ Session management
- ✅ Environment variables for secrets

### UI/UX
- ✅ Sky-blue themed design
- ✅ Glassmorphism effects
- ✅ Responsive (mobile-first)
- ✅ Smooth animations
- ✅ Bootstrap 5 styling
- ✅ Bootstrap Icons
- ✅ Success/error messages

### User Experience
- ✅ Form validation (client-side + server-side)
- ✅ Unique username/email checks
- ✅ Password match verification
- ✅ Terms & Conditions checkbox
- ✅ Auto-dismiss alerts
- ✅ Protected dashboard route

---

## 🛠 Tech Stack

### Backend
- **Framework**: Django 4.2
- **Database**: PostgreSQL 15
- **Authentication**: Django Auth + django-allauth
- **Environment Variables**: python-decouple

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Custom styles with animations
- **Bootstrap 5**: Responsive framework
- **JavaScript**: Vanilla JS (ES6+)
- **Icons**: Bootstrap Icons

### Development Tools
- **Python**: 3.10+
- **pip**: Package management
- **Virtual Environment**: venv

---

## 📁 Project Structure

```
ai_cartoon_generator/
│
├── ai_cartoon_project/          # Main Django project
│   ├── __init__.py
│   ├── settings.py              # Project settings
│   ├── urls.py                  # Root URL configuration
│   ├── wsgi.py                  # WSGI config
│   └── asgi.py                  # ASGI config
│
├── accounts/                    # Authentication app
│   ├── migrations/              # Database migrations
│   ├── __init__.py
│   ├── admin.py                 # Admin configuration
│   ├── apps.py                  # App configuration
│   ├── forms.py                 # Registration & Login forms
│   ├── models.py                # Custom User model
│   ├── signals.py               # OAuth signals
│   ├── tests.py                 # Unit tests
│   ├── urls.py                  # App URL configuration
│   └── views.py                 # Authentication views
│
├── templates/                   # HTML templates
│   ├── base.html               # Base template
│   └── accounts/
│       ├── register.html       # Registration page
│       ├── login.html          # Login page
│       └── dashboard.html      # Protected dashboard
│
├── static/                      # Static files
│   ├── css/
│   │   └── style.css           # Custom CSS
│   └── js/
│       └── script.js           # Custom JavaScript
│
├── media/                       # User uploads (future)
│
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
└── GOOGLE_OAUTH_SETUP.md       # OAuth setup guide
```

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+**: [Download Python](https://www.python.org/downloads/)
- **PostgreSQL 15+**: [Download PostgreSQL](https://www.postgresql.org/download/)
- **pip**: Comes with Python
- **virtualenv** (optional but recommended)

### Verify Installations

```bash
# Check Python version
python --version  # Should be 3.10 or higher

# Check PostgreSQL
psql --version

# Check pip
pip --version
```

---

## 🚀 Installation

### Step 1: Clone or Download the Project

```bash
# Navigate to the project directory
cd "C:\Users\Admin\OneDrive\Desktop\Infosys Springboard 6\ai_cartoon_generator"
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

This will install:
- Django 4.2+
- psycopg2-binary (PostgreSQL adapter)
- Pillow (image processing)
- django-allauth (Google OAuth)
- python-decouple (environment variables)
- gunicorn & whitenoise (production)

---

## ⚙️ Configuration

### Step 1: Create Environment File

```bash
# Copy the example environment file
copy .env.example .env

# On macOS/Linux:
cp .env.example .env
```

### Step 2: Generate Django Secret Key

```bash
# Generate a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 3: Edit .env File

Open `.env` and update the following:

```env
# Django Configuration
SECRET_KEY=your-generated-secret-key-from-step-2
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=ai_cartoon_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# Google OAuth (set these up later)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
```

---

## 🗄️ Database Setup

### Step 1: Create PostgreSQL Database

**Option A: Using psql (Command Line)**

```bash
# Open PostgreSQL prompt
psql -U postgres

# Create database
CREATE DATABASE ai_cartoon_db;

# Create user (optional)
CREATE USER ai_user WITH PASSWORD 'your_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE ai_cartoon_db TO ai_user;

# Exit
\q
```

**Option B: Using pgAdmin (GUI)**

1. Open pgAdmin
2. Right-click "Databases" → "Create" → "Database"
3. Name: `ai_cartoon_db`
4. Click "Save"

### Step 2: Run Django Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

This will create all necessary database tables.

### Step 3: Create Superuser (Admin)

```bash
# Create superuser account
python manage.py createsuperuser

# Follow the prompts:
# Username: admin
# Email: admin@example.com
# Password: (secure password)
```

---

## 🏃‍♂️ Running the Application

### Development Server

```bash
# Start the Django development server
python manage.py runserver

# Or specify a custom port
python manage.py runserver 8080
```

You should see:

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Access the Application

Open your browser and visit:

- **Login Page**: http://localhost:8000/accounts/login/
- **Register Page**: http://localhost:8000/accounts/register/
- **Dashboard**: http://localhost:8000/dashboard/ (requires login)
- **Admin Panel**: http://localhost:8000/admin/

---

## 🔐 Google OAuth Setup

To enable "Continue with Google" functionality, follow these steps:

### Quick Setup

1. **Read the detailed guide**: [GOOGLE_OAUTH_SETUP.md](GOOGLE_OAUTH_SETUP.md)

2. **Get Google OAuth credentials**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable Google+ API
   - Create OAuth 2.0 credentials
   - Copy Client ID and Client Secret

3. **Update .env file**:
   ```env
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret
   ```

4. **Configure Django Admin**:
   ```bash
   # Run server
   python manage.py runserver
   
   # Visit admin panel
   # http://localhost:8000/admin/
   
   # Add Social Application:
   # - Provider: Google
   # - Name: Google OAuth
   # - Client ID: (paste from Google Console)
   # - Secret key: (paste from Google Console)
   # - Sites: Select "localhost:8000"
   ```

5. **Test Google Login**:
   - Visit http://localhost:8000/accounts/login/
   - Click "Continue with Google"
   - Login with your Google account

**Full instructions**: See [GOOGLE_OAUTH_SETUP.md](GOOGLE_OAUTH_SETUP.md)

---

## 📝 Usage

### Register a New Account

1. Visit: http://localhost:8000/accounts/register/
2. Fill in the form:
   - Full Name
   - Username
   - Email
   - Password (min 8 chars, number + special char)
   - Confirm Password
   - Accept Terms & Conditions
3. Click "Create Account"
4. You'll be redirected to the login page

### Login

1. Visit: http://localhost:8000/accounts/login/
2. Enter username/email and password
3. Check "Remember me" (optional)
4. Click "Login"

### Login with Google

1. Visit: http://localhost:8000/accounts/login/
2. Click "Continue with Google"
3. Select your Google account
4. Grant permissions
5. Automatically redirected to dashboard

### Dashboard (Protected)

After login, you'll see:
- Welcome message with your name
- Profile information
- Upload image section (placeholder for future AI features)
- Profile picture (if logged in with Google)
- Logout button

### Logout

Click "Logout" in the navigation bar or visit:
http://localhost:8000/accounts/logout/

---

## 🧪 Testing

### Run Unit Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts

# Run with verbosity
python manage.py test --verbosity=2
```

### Manual Testing Checklist

- [ ] Register with valid data
- [ ] Register with existing username (should fail)
- [ ] Register with existing email (should fail)
- [ ] Register with weak password (should fail)
- [ ] Register with mismatched passwords (should fail)
- [ ] Login with username
- [ ] Login with email
- [ ] Login with invalid credentials (should fail)
- [ ] Login with Google OAuth
- [ ] Access dashboard when logged in
- [ ] Access dashboard when logged out (should redirect)
- [ ] Logout functionality
- [ ] Password visibility toggle
- [ ] Remember me functionality
- [ ] Form validation (client-side)
- [ ] Form validation (server-side)

---

## 🔒 Security Features

### Implemented Security Measures

1. **CSRF Protection**
   - All forms include `{% csrf_token %}`
   - Automatic Django middleware protection

2. **Password Security**
   - Hashed passwords (Django's PBKDF2 algorithm)
   - Strong password validation (8+ chars, number, special char)
   - Password confirmation

3. **Session Security**
   - Secure cookies in production
   - HTTP-only cookies
   - Session expiration

4. **Input Validation**
   - Client-side validation (JavaScript)
   - Server-side validation (Django forms)
   - SQL injection protection (Django ORM)
   - XSS protection (Django templates)

5. **Authentication**
   - Login required decorators
   - Protected routes
   - OAuth 2.0 for Google Sign-In

6. **Environment Variables**
   - Secrets stored in `.env`
   - `.env` excluded from Git

### Security Best Practices

- Never commit `.env` to version control
- Use strong SECRET_KEY in production
- Enable HTTPS in production
- Set `DEBUG=False` in production
- Rotate secrets regularly
- Keep dependencies updated

---

## 🌐 Deployment

### Prepare for Production

1. **Update .env**:
   ```env
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   SECRET_KEY=generate-new-secure-key
   ```

2. **Collect Static Files**:
   ```bash
   python manage.py collectstatic
   ```

3. **Update Google OAuth**:
   - Add production domain to authorized origins
   - Add production callback URL

### Deploy to Heroku (Example)

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create Heroku app
heroku create ai-cartoon-generator

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY=your-production-secret-key
heroku config:set DEBUG=False
heroku config:set GOOGLE_CLIENT_ID=your-client-id
heroku config:set GOOGLE_CLIENT_SECRET=your-client-secret

# Push to Heroku
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# Open app
heroku open
```

### Other Deployment Options

- **AWS EC2**: Traditional server deployment
- **DigitalOcean**: App Platform or Droplets
- **Google Cloud**: App Engine or Compute Engine
- **Azure**: App Service
- **PythonAnywhere**: Easy Django hosting

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'accounts'`

**Solution**: Make sure you're in the project directory and virtual environment is activated.

---

**Issue**: `psycopg2.OperationalError: FATAL: database "ai_cartoon_db" does not exist`

**Solution**: Create the PostgreSQL database (see Database Setup section).

---

**Issue**: `ImproperlyConfigured: The SECRET_KEY setting must not be empty`

**Solution**: Check that `.env` file exists and has a valid `SECRET_KEY`.

---

**Issue**: Google OAuth redirect URI mismatch

**Solution**: Ensure your redirect URI in Google Console is exactly:
```
http://localhost:8000/auth/google/login/callback/
```

---

**Issue**: Static files (CSS/JS) not loading

**Solution**: 
```bash
# Collect static files
python manage.py collectstatic

# Or set STATICFILES_DIRS in settings.py
```

---

**Issue**: Port 8000 already in use

**Solution**:
```bash
# Use a different port
python manage.py runserver 8080
```

---

### Getting Help

If you encounter issues:

1. Check Django logs in the terminal
2. Check browser console for JavaScript errors
3. Verify all setup steps were completed
4. Ensure virtual environment is activated
5. Check PostgreSQL is running
6. Review error messages carefully

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/AmazingFeature`
3. **Commit your changes**: `git commit -m 'Add some AmazingFeature'`
4. **Push to the branch**: `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Write docstrings for functions
- Keep functions small and focused

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Django**: Web framework
- **Bootstrap**: CSS framework
- **PostgreSQL**: Database
- **django-allauth**: Social authentication
- **Google**: OAuth provider

---

## 📞 Contact

For questions or support:

- **Email**: support@aicartoon.com
- **GitHub Issues**: [Create an issue](https://github.com/yourusername/ai-cartoon-generator/issues)

---

## 🎯 Next Steps

This authentication system is ready for the AI image processing features:

### Future Development
1. **AI Cartoon Transformation**
   - Image upload functionality
   - AI model integration (TensorFlow/PyTorch)
   - Image processing pipeline
   
2. **User Features**
   - Profile editing
   - Password reset
   - Email verification
   - Account deletion

3. **Gallery**
   - Save transformed images
   - View history
   - Download images
   - Share on social media

4. **Advanced Features**
   - Multiple cartoon styles
   - Batch processing
   - API for developers
   - Mobile app

---

## ⭐ Quick Start Summary

```bash
# 1. Navigate to project
cd ai_cartoon_generator

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env from template
copy .env.example .env

# 5. Create PostgreSQL database
psql -U postgres -c "CREATE DATABASE ai_cartoon_db;"

# 6. Run migrations
python manage.py migrate

# 7. Create superuser
python manage.py createsuperuser

# 8. Run server
python manage.py runserver

# 9. Visit http://localhost:8000/accounts/login/
```

---

**✨ You're all set! Start building amazing AI-powered cartoon transformations!** 🎨

---

Made with ❤️ by AI Cartoon Generator Team
