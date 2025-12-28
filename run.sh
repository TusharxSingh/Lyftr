#!/bin/bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Start server at http://localhost:8000
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

