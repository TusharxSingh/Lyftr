@echo off
REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
pip install -r requirements.txt

REM Install Playwright browsers
playwright install chromium

REM Start server at http://localhost:8000
REM Use start_server.py to fix asyncio issues with Playwright
python start_server.py

