@echo off

REM Activate the virtual environment
call .venv\Scripts\activate

REM Run the Flask application
python app.py

REM Optional: Pause to see the output
pause