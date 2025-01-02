"""
Dynamic theme generator for NoteGenius UI.
Features:
- Customizable color scheme based on primary color
- Consistent styling across all UI components
- Support for both light and dark modes
- Dynamic theme updates without restart
"""

import json
from pathlib import Path
from config import INTERFACE_SETTINGS

def generate_theme():
    """Generates theme.json file with primary color from config."""
    primary_color = INTERFACE_SETTINGS["primary_color"]
    
    theme = {
        "CTk": {
            "fg_color": ["#ffffff", "#ffffff"]
        },
        "CTkFont": {
            "family": "Helvetica",
            "size": 13,
            "weight": "bold"
        },
        "DropdownMenu": {
            "fg_color": ["#ffffff", "gray20"],
            "hover_color": ["#F0F0F0", "gray28"],
            "text_color": ["gray14", "gray84"],
            "font": {"family": "Helvetica", "size": 13, "weight": "bold"}
        },
        "CTkScrollbar": {
            "corner_radius": 6,
            "border_spacing": 4,
            "fg_color": "transparent",
            "button_color": ["gray55", "gray41"],
            "button_hover_color": ["gray40", "gray53"]
        },
        "CTkButton": {
            "corner_radius": 6,
            "border_width": 1,
            "fg_color": ["white", "white"],
            "hover_color": ["#E0DBF5", "#E0DBF5"],
            "border_color": [primary_color, primary_color],
            "text_color": [primary_color, primary_color],
            "text_color_disabled": ["white", "white"],
            "font": {"family": "Helvetica", "size": 13, "weight": "bold"},
            "height": 36,
            "width": 36
        },
        "CTkEntry": {
            "corner_radius": 6,
            "border_width": 2,
            "fg_color": ["#ffffff", "gray24"],
            "border_color": ["#C2B8E8", "#C2B8E8"],
            "text_color": ["gray14", "gray84"],
            "placeholder_text_color": ["gray52", "gray62"],
            "font": {"family": "Helvetica", "size": 13, "weight": "bold"},
            "height": 36
        },
        "CTkFrame": {
            "corner_radius": 6,
            "border_width": 0,
            "fg_color": ["gray95", "gray16"],
            "top_fg_color": [primary_color, primary_color],
            "border_color": ["#C2B8E8", "#C2B8E8"]
        },
        "CTkLabel": {
            "corner_radius": 0,
            "fg_color": "transparent",
            "text_color": ["gray14", "gray84"],
            "font": {"family": "Helvetica", "size": 13, "weight": "bold"}
        },
        "CTkOptionMenu": {
            "corner_radius": 6,
            "fg_color": [primary_color, primary_color],
            "button_color": [primary_color, primary_color],
            "button_hover_color": [primary_color, primary_color],
            "text_color": ["#ffffff", "#ffffff"],
            "text_color_disabled": ["gray74", "gray60"],
            "font": {"family": "Helvetica", "size": 13, "weight": "bold"}
        },
        "CTkTextbox": {
            "corner_radius": 6,
            "border_width": 2,
            "fg_color": ["#ffffff", "gray24"],
            "border_color": ["#C2B8E8", "#C2B8E8"],
            "text_color": ["gray14", "gray84"],
            "scrollbar_button_color": ["gray55", "gray41"],
            "scrollbar_button_hover_color": ["gray40", "gray53"],
            "font": {"family": "Helvetica", "size": 13, "weight": "bold"},
            "placeholder_text_color": ["gray52", "gray62"]
        },
        "CTkProgressBar": {
            "corner_radius": 6,
            "border_width": 0,
            "fg_color": ["#F0F0F0", "#F0F0F0"],
            "progress_color": [primary_color, primary_color],
            "border_color": ["#C2B8E8", "#C2B8E8"]
        }
    }
    
    # Ensure theme directory exists
    theme_dir = Path(__file__).parent
    theme_dir.mkdir(exist_ok=True)
    
    # Save theme
    theme_path = theme_dir / "theme.json"
    with open(theme_path, "w") as f:
        json.dump(theme, f, indent=2)