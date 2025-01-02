"""
Main entry point for the NoteGenius application.
Sets up the necessary environment and launches the GUI.
"""

import customtkinter as ctk
from interface import NoteGenius
from processor import ContentProcessor
from pathlib import Path
import os
import sys
from theme.theme_generator import generate_theme

def setup_directories():
    """Creates the cache directory for storing YouTube transcriptions."""
    directories = ['cache']
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)

def check_environment():
    """
    Verifies if the required environment variables are set.
    Currently checks for GOOGLE_API_KEY which is needed for Gemini AI.
    """
    required_vars = ['GOOGLE_API_KEY']
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"Missing environment variables: {', '.join(missing)}")

def main():
    """
    Main function that:
    1. Sets up required directories
    2. Checks environment variables
    3. Generates the theme
    4. Initializes and runs the GUI
    """
    try:
        setup_directories()
        check_environment()
        generate_theme()
        
        root = ctk.CTk()
        processor = ContentProcessor()
        app = NoteGenius(root, processor)
        root.mainloop()
        
    except Exception as e:
        import tkinter.messagebox as messagebox
        messagebox.showerror("Initialization Error", str(e))
        sys.exit(1)

if __name__ == "__main__":
    main() 