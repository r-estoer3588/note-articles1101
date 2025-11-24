@echo off
echo Starting Buffer Monitoring Dashboard (with API Server)...
echo.
echo 1. Starting local server with write access...
echo 2. Opening dashboard in browser...
echo.
echo NOTE: Keep this window open to allow saving data.
echo.

cd /d "%~dp0"
start "" "http://localhost:8000/dashboard.html"
python server.py
