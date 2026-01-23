@echo off
echo ========================================
echo   Quick Test - Twilio Auth System
echo ========================================
echo.
echo This will:
echo 1. Check if backend is running
echo 2. Test Twilio configuration
echo 3. Open login page
echo.
pause

cd /d "%~dp0"

echo.
echo Checking backend status...
curl -s http://localhost:8000/health > nul 2>&1
if %errorlevel% == 0 (
    echo ✓ Backend is running
) else (
    echo ✗ Backend is NOT running
    echo.
    echo Please start backend first:
    echo   start_backend.bat
    echo.
    pause
    exit /b
)

echo.
echo Testing Twilio configuration...
python Backend\test_twilio_auth.py

echo.
echo ========================================
echo   Opening Login Page
echo ========================================
echo.
echo Login page: http://localhost:5173/login
echo.
echo Instructions:
echo 1. Enter your 10-digit phone number
echo 2. Click "OTP भेजें"
echo 3. Check your phone for SMS
echo 4. Enter the 6-digit OTP
echo 5. Click "सत्यापित करें और लॉगिन करें"
echo.
echo If in MOCK MODE:
echo - OTP will be shown in alert popup
echo - OTP will be in console
echo - Check yellow debug box on page
echo.
pause

start http://localhost:5173/login

echo.
echo Login page opened in browser!
echo.
pause
