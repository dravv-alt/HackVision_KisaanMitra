@echo off
echo ========================================
echo   Starting KisanMitra Backend
echo ========================================
echo.

cd /d "%~dp0"
set PYTHONPATH=%CD%

echo PYTHONPATH set to: %PYTHONPATH%
python -m uvicorn Backend.api.main:app --reload --port 8000
pause
