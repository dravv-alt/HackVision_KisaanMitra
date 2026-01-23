@echo off
echo ========================================
echo   Testing Twilio Authentication
echo ========================================
echo.
echo Step 1: Installing dependencies...
cd Backend
pip install twilio PyJWT python-dotenv --quiet
echo.
echo Step 2: Testing Twilio configuration...
python test_twilio_auth.py
echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start backend: start_backend.bat
echo 2. Start frontend: cd Frontend\kisanmitra-app ^&^& npm run dev
echo 3. Visit: http://localhost:5173/login
echo.
pause
