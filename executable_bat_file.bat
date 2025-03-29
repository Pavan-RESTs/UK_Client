@echo off

REM Activate the virtual environment
call conda activate base

REM Run the Flask application
python app.py

REM Optional: Pause to see the output
pause