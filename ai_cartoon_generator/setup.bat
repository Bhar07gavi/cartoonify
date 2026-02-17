@echo off
REM ========================================
REM AI Cartoon Generator - Quick Setup Script
REM For Windows
REM ========================================

echo.
echo ======================================
echo   AI Cartoon Generator - Setup
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/7] Python detected...
echo.

REM Create virtual environment
if not exist "venv" (
    echo [2/7] Creating virtual environment...
    python -m venv venv
    echo Virtual environment created successfully!
) else (
    echo [2/7] Virtual environment already exists, skipping...
)
echo.

REM Activate virtual environment
echo [3/7] Activating virtual environment...
call venv\Scripts\activate
echo.

REM Upgrade pip
echo [4/7] Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo [5/7] Installing dependencies...
pip install -r requirements.txt
echo.

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo [6/7] Creating .env file from template...
    copy .env.example .env
    echo.
    echo [IMPORTANT] Please edit the .env file with your database credentials
    echo            and generate a new SECRET_KEY
    echo.
) else (
    echo [6/7] .env file already exists, skipping...
    echo.
)

REM Display next steps
echo [7/7] Setup Complete!
echo.
echo ======================================
echo   Next Steps:
echo ======================================
echo.
echo 1. Edit .env file with your settings:
echo    - Update DB_PASSWORD
echo    - Generate SECRET_KEY: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
echo.
echo 2. Create PostgreSQL database:
echo    psql -U postgres -c "CREATE DATABASE ai_cartoon_db;"
echo.
echo 3. Run migrations:
echo    python manage.py migrate
echo.
echo 4. Create superuser:
echo    python manage.py createsuperuser
echo.
echo 5. Run the development server:
echo    python manage.py runserver
echo.
echo 6. Visit: http://localhost:8000/accounts/login/
echo.
echo ======================================
echo.

pause
