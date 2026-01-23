@echo off
echo ========================================
echo   KisanMitra - Complete System Launch
echo ========================================
echo.
echo This will start:
echo 1. MongoDB Server
echo 2. Backend API Server
echo 3. Frontend Development Server
echo.
echo Make sure MongoDB is installed!
echo.
pause

cd /d "%~dp0"

echo.
echo ========================================
echo   Step 1: Starting MongoDB Server
echo ========================================
echo.

REM Start MongoDB in a new window
start "MongoDB Server" cmd /k "mongod --dbpath C:\data\db || echo MongoDB failed to start. Make sure it's installed and dbpath exists."

echo MongoDB starting in new window...
timeout /t 3 /nobreak > nul

echo.
echo ========================================
echo   Step 2: Starting Backend API Server
echo ========================================
echo.

REM Set PYTHONPATH to current directory so 'Backend' module is found
set PYTHONPATH=%CD%

REM Start Backend from root using full module path
start "Backend API Server" cmd /k "python -m uvicorn Backend.api.main:app --reload --port 8000"

echo Backend API starting on http://localhost:8000
echo Swagger UI will be available at http://localhost:8000/docs
timeout /t 5 /nobreak > nul

echo.
echo ========================================
echo   Step 3: Starting Frontend Dev Server
echo ========================================
echo.

REM Start Frontend in a new window
start "Frontend Dev Server" cmd /k "cd Frontend\kisanmitra-app && npm run dev"

echo Frontend starting on http://localhost:5173
timeout /t 3 /nobreak > nul

echo.
echo ========================================
echo   All Services Started!
echo ========================================
echo.
echo MongoDB:  Running in separate window
echo Backend:  http://localhost:8000
echo Swagger:  http://localhost:8000/docs
echo Frontend: http://localhost:5173
echo Login:    http://localhost:5173/login
echo.
echo Press any key to open the application in browser...
pause > nul

REM Open browser
start http://localhost:5173/login

echo.
echo ========================================
echo   System Running!
echo ========================================
echo.
echo To stop all services:
echo - Close all the command windows
echo - Or run: stop_all_services.bat
echo.
echo This window can be closed safely.
echo.
pause
