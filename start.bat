@echo off
echo Starting AI Food Nutrition Analyzer Backend...
cd /d "%~dp0"

:: Check if virtual environment exists, if not create it
if not exist .venv (
    echo Creating Python virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo Error: Python is not installed or not in PATH. Please install Python.
        pause
        exit /b 1
    )
)

:: Install dependencies
echo Checking/Installing requirements...
.venv\Scripts\pip.exe install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies.
    pause
    exit /b 1
)

:: Initialize database if not exists
if not exist data\nutrition.db (
    echo Initializing database...
    .venv\Scripts\python.exe initialize_db.py
    if errorlevel 1 (
        echo Error: Database initialization failed.
        pause
        exit /b 1
    )
)

:: Open the app in the default browser
start "" http://127.0.0.1:5500

:: Start Uvicorn
echo Starting server...
.venv\Scripts\uvicorn.exe main:app --reload --host 127.0.0.1 --port 5500
pause
