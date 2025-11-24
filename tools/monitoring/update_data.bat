@echo off
echo Fetching data from Buffer...
python fetch_data.py
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Success! Data updated.
    timeout /t 3
) else (
    echo.
    echo Failed to update data.
    pause
)
