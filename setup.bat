@echo off
echo ========================================
echo Wildlife Monitoring AI - Setup Script
echo ========================================
echo.

echo [1/3] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
echo.

echo [2/3] Installing Python dependencies...
cd backend
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
cd ..
echo.

echo [3/3] Setup complete!
echo.
echo ========================================
echo To start the application:
echo   1. cd backend
echo   2. python app.py
echo   3. Open browser to http://localhost:5000
echo ========================================
echo.
pause
