@echo off
REM INF232 EC2 - Setup Script for Windows

echo ================================
echo INF232 EC2 - Setup Script
echo ================================
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
echo Virtual environment created.
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated.
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo Dependencies installed.
echo.

REM Initialize database
echo Initializing database...
python -c "from app import init_db; init_db()"
echo Database initialized.
echo.

echo ================================
echo Setup Complete!
echo ================================
echo.
echo To start the application, run:
echo   venv\Scripts\activate.bat
echo   python app.py
echo.
echo Then open your browser and navigate to:
echo   http://localhost:5000
echo.
pause
