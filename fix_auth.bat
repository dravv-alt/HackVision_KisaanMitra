@echo off
echo ========================================
echo   Auth System Diagnostic and Fix
echo ========================================
echo.

cd /d "%~dp0"

echo Running diagnostic...
echo.
python Backend\diagnose_auth.py

echo.
echo ========================================
echo   Installing/Updating Dependencies
echo ========================================
echo.

cd Backend
pip install --upgrade twilio PyJWT python-dotenv pymongo fastapi uvicorn

echo.
echo ========================================
echo   Testing Backend Startup
echo ========================================
echo.

echo Starting backend for 5 seconds to check for errors...
timeout /t 2 /nobreak > nul

set PYTHONPATH=%CD%
start /B python -m uvicorn Backend.api.main:app --port 8000 > backend_test.log 2>&1
set BACKEND_PID=%ERRORLEVEL%

timeout /t 5 /nobreak

echo.
echo Checking backend_test.log for errors...
type backend_test.log

taskkill /F /IM python.exe > nul 2>&1

echo.
echo ========================================
echo   Fix Complete!
echo ========================================
echo.
echo If you see errors above, please share them.
echo Otherwise, try starting the backend again:
echo   start_backend.bat
echo.
pause
