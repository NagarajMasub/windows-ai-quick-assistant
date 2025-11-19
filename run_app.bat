@echo off
REM Activate virtual environment and run the app silently
cd /d "%~dp0"
call venv\Scripts\activate.bat
start /b venv\Scripts\pythonw.exe ai_grammar_checker.pyw
echo AI Grammar Checker started in background.
echo Press Ctrl+Shift+R after copying text to rephrase it.
timeout /t 3 >nul
