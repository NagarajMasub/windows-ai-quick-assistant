@echo off
echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo To run the application:
echo   1. venv\Scripts\activate.bat
echo   2. pythonw ai_grammar_checker.pyw
echo.
echo Or simply double-click: run_app.bat
pause
