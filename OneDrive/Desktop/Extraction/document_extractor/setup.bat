@echo off
REM Development setup script for Document Extraction Platform (Windows)

echo ===================================
echo Document Extractor - Setup Script
echo ===================================
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Create directories
echo Creating uploads and logs directories...
if not exist uploads mkdir uploads
if not exist logs mkdir logs
echo.

REM Setup environment file
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo WARNING: Please update .env with your configuration
    echo   - DATABASE_URL
    echo   - OPENAI_API_KEY
) else (
    echo .env file already exists
)
echo.

echo ===================================
echo Setup Complete!
echo ===================================
echo.
echo Next steps:
echo 1. Update .env with your configuration
echo 2. Ensure PostgreSQL is running
echo 3. Start backend: uvicorn app.main:app --reload
echo 4. Start UI: streamlit run streamlit_app.py
echo.
pause
