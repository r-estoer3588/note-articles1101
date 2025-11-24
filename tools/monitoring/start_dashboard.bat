@echo off
echo Starting Buffer Monitoring Dashboard...
echo.
echo 1. Starting local server...
echo 2. Opening dashboard in browser...
echo.
echo NOTE: Keep this window open while using the dashboard.
echo Close this window to stop the server.
echo.

cd /d "%~dp0"
start "" "http://localhost:8000/dashboard.html"
python -m http.server 8000
