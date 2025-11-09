@echo off
chcp 65001 >nul
echo ========================================
echo LINE Bot Setup Check
echo ========================================
echo.

REM Check Python
echo [1/5] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found
    exit /b 1
)
python --version
echo [OK]
echo.

REM Check pandas
echo [2/5] Checking pandas...
python -c "import pandas" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] pandas not installed
    echo Installing pandas...
    pip install pandas
) else (
    echo [OK]
)
echo.

REM Test helper script
echo [3/5] Testing line_bot_helper.py...
python line_bot_helper.py today_theme
if %errorlevel% neq 0 (
    echo [ERROR] Helper script failed
    exit /b 1
)
echo [OK]
echo.

REM Test algorithm
echo [4/5] Testing hogey_algorithm.py...
python hogey_algorithm.py --count 1 --theme "test" --output test_setup.csv >nul 2>&1
if exist test_setup.csv (
    echo [OK]
    del test_setup.csv
) else (
    echo [ERROR] Algorithm test failed
)
echo.

REM Open guide
echo [5/5] Opening setup guide...
start QUICK_START_GUIDE.md
echo [OK]
echo.

echo ========================================
echo Setup check complete!
echo ========================================
echo.
echo Next steps:
echo 1. Follow QUICK_START_GUIDE.md
echo 2. Setup LINE Developers (15 min)
echo 3. Setup Google Sheets (10 min)
echo 4. Create rich menu (10 min)
echo 5. Configure n8n (15 min)
echo.
echo Total time: 40-50 minutes
echo.

pause
