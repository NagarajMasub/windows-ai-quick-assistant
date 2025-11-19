"""
AI Grammar Checker & Text Rephraser
====================================

A background service that corrects grammar and improves text clarity using Google's Gemini API.

Usage:
    1. Copy text normally with Ctrl+C
    2. Press Ctrl+Shift+R to trigger grammar correction
    3. Wait for notification "Rephrased text ready!"
    4. Paste corrected text with Ctrl+V

Features:
    - Works in all applications (Teams, Outlook, Chrome, Word, etc.)
    - Non-intrusive clipboard-based workflow
    - Windows toast notifications for feedback
    - Runs silently in background

Requirements:
    - Python 3.7+
    - google-generativeai
    - pynput
    - pywin32
    - win10toast
    - pip-system-certs (for corporate networks)
    - certifi

Setup:
    1. Set GOOGLE_API_KEY environment variable with your Gemini API key
    2. Install dependencies: pip install -r requirements.txt
    3. Run: pythonw ai_grammar_checker.pyw

Author: Your Name
License: MIT
"""

import time
from pynput import keyboard
import pyperclip
import threading
import os
import certifi
from winotify import Notification

# Fix SSL certificate issues for corporate environments
import pip_system_certs.wrapt_requests

# Set certificate paths for HTTPS requests
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

import google.generativeai as genai

# Global state
processing = False

# ============================================================================
# Clipboard Management
# ============================================================================

def get_clipboard():
    """
    Safely retrieve text from Windows clipboard.
    
    Returns:
        str: Clipboard text content, or empty string if clipboard is empty or error occurs
    """
    try:
        return pyperclip.paste()
    except Exception:
        return ""

def set_clipboard(text):
    """
    Safely set text to Windows clipboard.
    
    Args:
        text (str): Text to copy to clipboard
    """
    try:
        pyperclip.copy(text)
    except Exception:
        pass

# ============================================================================
# Gemini API Configuration
# ============================================================================

# Get API key from environment variable
GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')

if not GEMINI_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY environment variable not set. "
        "Please set it with your Gemini API key."
    )

# Configure Gemini with REST transport for better corporate network compatibility
genai.configure(api_key=GEMINI_API_KEY, transport='rest')  # type: ignore

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.5-flash')  # type: ignore

# ============================================================================
# Text Processing
# ============================================================================

def rephrase_text(text):
    """
    Correct grammar and improve clarity of text using Gemini API.
    
    Args:
        text (str): Original text to be corrected
        
    Returns:
        str: Grammar-corrected and improved text, or original text if API fails
    """
    try:
        prompt = f"""Please correct the grammar and improve the clarity of the following text. Return only the corrected text without any explanations or additional comments:

{text}"""
        
        # Call Gemini API
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        # If API fails, return original text
        # Could log error here for debugging
        return text

# ============================================================================
# Hotkey Handler
# ============================================================================

def on_hotkey():
    """
    Handle Ctrl+Shift+R hotkey press.
    Triggers text processing in a separate thread to avoid blocking the listener.
    """
    global processing
    
    # Prevent re-entry if already processing
    if processing:
        return
    
    processing = True
    
    # Run in separate thread to keep hotkey listener responsive
    thread = threading.Thread(target=process_clipboard_text)
    thread.daemon = True
    thread.start()

def process_clipboard_text():
    """
    Main processing workflow:
    1. Read current clipboard
    2. Send to Gemini for grammar correction
    3. Put corrected text back in clipboard
    4. Show notification
    """
    global processing
    
    try:
        # Get current clipboard content
        clipboard_text = get_clipboard()
        
        # Validate clipboard has text content
        if not clipboard_text or not clipboard_text.strip():
            toast = Notification(
                app_id="AI Grammar Checker",
                title="AI Grammar Checker",
                msg="No text found in clipboard. Copy some text first!",
                duration="short"
            )
            toast.show()
            return
        
        # Show processing notification
        toast = Notification(
            app_id="AI Grammar Checker",
            title="AI Grammar Checker",
            msg="Processing your text...",
            duration="short"
        )
        toast.show()
        
        # Process text with Gemini API
        corrected_text = rephrase_text(clipboard_text)
        
        # Put corrected text back in clipboard
        set_clipboard(corrected_text)
        
        # Show success notification
        toast = Notification(
            app_id="AI Grammar Checker",
            title="AI Grammar Checker",
            msg="✓ Rephrased text ready! Press Ctrl+V to paste.",
            duration="long"
        )
        toast.show()
    
    except Exception as e:
        # Show error notification
        toast = Notification(
            app_id="AI Grammar Checker",
            title="AI Grammar Checker",
            msg=f"Error: {str(e)}",
            duration="long"
        )
        toast.show()
    
    finally:
        # Reset processing flag
        time.sleep(0.2)
        processing = False

# ============================================================================
# Main Application
# ============================================================================

def main():
    """
    Initialize and run the hotkey listener.
    Listens for Ctrl+Shift+R globally across all applications.
    """
    # Show startup notification
    toast = Notification(
        app_id="AI Grammar Checker",
        title="AI Grammar Checker",
        msg="Running! Press Ctrl+Shift+R to rephrase copied text.",
        duration="long"
    )
    toast.show()
    
    # Set up the hotkey listener for Ctrl+Shift+R
    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse('<ctrl>+<shift>+r'),
        on_hotkey
    )
    
    # Helper function to normalize key events
    def for_canonical(f):
        return lambda k: f(listener.canonical(k))
    
    # Start keyboard listener
    # This will block until the program is terminated
    with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)
    ) as listener:
        listener.join()

# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    main()
