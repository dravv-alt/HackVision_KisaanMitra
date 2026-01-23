@echo off
echo ========================================
echo   Stopping All KisanMitra Services
echo ========================================
echo.

REM Kill MongoDB
echo Stopping MongoDB...
taskkill /F /IM mongod.exe 2>nul
if %errorlevel% == 0 (
    echo MongoDB stopped.
) else (
    echo MongoDB was not running.
)

REM Kill Python (Backend)
echo Stopping Backend API Server...
taskkill /F /IM python.exe 2>nul
if %errorlevel% == 0 (
    echo Backend stopped.
) else (
    echo Backend was not running.
)

REM Kill Node (Frontend)
echo Stopping Frontend Dev Server...
taskkill /F /IM node.exe 2>nul
if %errorlevel% == 0 (
    echo Frontend stopped.
) else (
    echo Frontend was not running.
)

echo.
echo ========================================
echo   All Services Stopped!
echo ========================================
echo.
pause
