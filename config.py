"""
Central configuration file for NoteGenius.
Contains all settings, paths, and prompts used throughout the application.
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Verify Google API key existence
if not os.getenv('GOOGLE_API_KEY'):
    raise EnvironmentError("GOOGLE_API_KEY not found in .env file")

# Directory configurations
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = Path(r"Obsidian vault path or any other directory")  
CACHE_DIR = BASE_DIR / "cache"  # For storing YouTube transcriptions
ASSETS_DIR = BASE_DIR / "assets"  # For application assets like logos

# LLM Model configuration
LLM_MODEL = "gemini-2.0-flash-exp"

# File type settings for PDF file dialog
SUPPORTED_FILETYPES = [
    ('PDF files', '*.pdf'),
    ('Text files', '*.txt'),
    ('All files', '*.*')
]

# Supported languages for note generation
LANGUAGES = {
    "portuguese": "Portuguese",
    "english": "English",
    "spanish": "Spanish",
}

# Available input types
INPUT_TYPES = [
    "PDF File",
    "YouTube Link", 
    "Website URL",
    "Manual Input"
]

# Layout configurations with their specific prompts
LAYOUTS = {
    "video": {
        "name": "Video",
        "prompt": """
            Detailed prompt for video content...
        """
    },
    "Article": {
        "name": "Article",
        "prompt": """
            Detailed prompt for Article content...
        """
    },
    "Book": {
        "name": "Book",
        "prompt": """
            Detailed prompt for Book content...
        """
    },
}

# Base prompt template used for all content processing
BASE_PROMPT = """
{prefix}
... prompt template ...
{content_section}
"""

# UI settings
INTERFACE_SETTINGS = {
    "window_title": "NoteGenius",
    "window_size": "600x850",
    "theme_mode": "system",
    "primary_color": "#725DD2",
    "hover_color": "#5E4CAD",
    "button_height": 28,
    "language_button_width": 100,
    "layout_button_width": 80,
    "button_spacing": 5,
    # "logo": { #if you dont have a logo, remove this section
    #     "path": ASSETS_DIR / "logo.png",
    #     "size": (60, 60)
    #}
}