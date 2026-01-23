@echo off
echo ========================================
echo   KisanMitra Mock Data Generator
echo ========================================
echo.
echo This will populate MongoDB with comprehensive mock data
echo - 25 Farmers
echo - 30 Crops
echo - 30 Active Crops
echo - 25 Equipment Listings
echo - 20 Government Schemes
echo - 30 Financial Transactions
echo - 25 Market Prices
echo - 20 Weather Records
echo - 25 Alerts
echo - 30 Calendar Events
echo.
echo WARNING: This will DELETE existing data!
echo.
pause

cd /d "%~dp0"
python Backend\database\insert_mock_data.py

echo.
echo ========================================
echo   Mock Data Insertion Complete!
echo ========================================
pause
