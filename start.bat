@echo off
echo ========================================
echo Starting Wildlife Monitoring AI Server
echo ========================================
echo.

cd backend
echo Server starting at http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py
