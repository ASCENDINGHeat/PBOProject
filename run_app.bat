@echo off
REM Install dependencies if not already installed
pip install --upgrade pip
pip install -r requirements.txt

REM Run the app
python Main.py
pause