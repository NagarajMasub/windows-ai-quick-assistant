# AI Grammar Checker & Text Rephraser

A lightweight Windows background service that corrects grammar and improves text clarity using Google's Gemini AI. Works seamlessly with any application including Teams, Outlook, Chrome, Word, and more.

## Features

- ✅ **Universal Compatibility**: Works in all Windows applications
- 🔒 **Non-Intrusive**: Clipboard-based workflow with no keyboard simulation
- 🔔 **User Feedback**: Windows toast notifications for status updates
- 🚀 **Fast**: Processes text in background without blocking
- 🌐 **Corporate Network Support**: Handles SSL certificates for enterprise environments
- 💡 **Simple Workflow**: Copy → Press hotkey → Paste

## How It Works

1. **Copy** text normally with `Ctrl+C`
2. **Press** `Ctrl+Shift+R` to trigger grammar correction
3. **Wait** for notification "Rephrased text ready!"
4. **Paste** corrected text with `Ctrl+V`

## Prerequisites

- Windows 10/11
- Python 3.7 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd rephraseAi
```

### 2. Run setup script

**Windows (Automated):**
```bash
setup.bat
```

This will:
- Create a virtual environment in `venv/` folder
- Install all dependencies
- Configure everything automatically

**Manual Setup:**
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

### 3. Set up API key

**Option A: Environment Variable (Recommended)**
```bash
setx GOOGLE_API_KEY "your-api-key-here"
```

**Option B: System Environment Variables**
1. Open System Properties → Advanced → Environment Variables
2. Add new user variable: `GOOGLE_API_KEY` with your API key
3. Restart your terminal/IDE

### 4. Run the application

**Easy way (Recommended):**
- Double-click `run_silent.vbs` (runs in background, no console)
- Or double-click `run_app.bat` (shows startup message)

**Manual way:**
```bash
# Activate virtual environment first
venv\Scripts\activate.bat

# Run in background (no console)
venv\Scripts\pythonw.exe ai_grammar_checker.pyw

# Or run with console (for debugging)
venv\Scripts\python.exe ai_grammar_checker.pyw
```

## Usage Example

### In Microsoft Teams:
```
Original text: "me and my frend is going to store"
1. Select and copy: Ctrl+C
2. Press: Ctrl+Shift+R
3. Wait for notification
4. Paste: Ctrl+V
Result: "My friend and I are going to the store"
```

## Configuration

### Change Hotkey

Edit `ai_grammar_checker.pyw` line 236:
```python
keyboard.HotKey.parse('<ctrl>+<shift>+r')  # Change to your preferred key combo
```

### Change AI Model

Edit `ai_grammar_checker.pyw` line 112:
```python
model = genai.GenerativeModel('gemini-2.5-flash')  # Try 'gemini-pro' or others
```

### Customize Prompt

Edit `ai_grammar_checker.pyw` in the `rephrase_text()` function to change how AI processes text.

## Troubleshooting

### "GOOGLE_API_KEY environment variable not set"
- Ensure you've set the environment variable correctly
- Restart your terminal/IDE after setting it
- Verify with: `echo %GOOGLE_API_KEY%`

### "Import winotify could not be resolved"
```bash
pip install winotify
```

### SSL Certificate Errors
The app includes `pip-system-certs` for corporate networks. If issues persist:
```bash
pip install --upgrade pip-system-certs certifi
```

## Stopping the Application

1. Open Task Manager (`Ctrl+Shift+Esc`)
2. Find `pythonw.exe` or `python.exe`
3. End the process



