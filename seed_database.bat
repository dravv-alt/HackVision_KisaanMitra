@echo off
echo ========================================
echo KisanMitra - Database Seeding
echo ========================================
echo.

cd /d "%~dp0.."
python Backend\database\seed_data.py

echo.
echo ========================================
echo Press any key to exit...
pause >nul
