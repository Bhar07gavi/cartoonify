@echo off
REM ========================================
REM AI Cartoon Generator - Run Script
REM For Windows
REM ========================================

echo.
echo ======================================
echo   AI Cartoon Generator
echo   Starting Development Server...
echo ======================================
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate
    echo Virtual environment activated
    echo.
) else (
    echo [WARNING] Virtual environment not found!
    echo Please run setup.bat first
    echo.
    pause
    exit /b 1
)

REM Check if migrations are needed
echo Checking for pending migrations...
python manage.py showmigrations | findstr /C:"[ ]" >nul
if %errorlevel% equ 0 (
    echo [INFO] Pending migrations detected. Run: python manage.py migrate
    echo.
)

REM Run development server
echo Starting Django development server...
echo.
echo ======================================
echo   Server will start at:
echo   http://localhost:8000/
echo.
echo   Login Page:
echo   http://localhost:8000/accounts/login/
echo.
echo   Press Ctrl+C to stop the server
echo ======================================
echo.

python manage.py runserver
