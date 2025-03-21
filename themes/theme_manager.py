import json
import os

theme_file = os.path.join(os.path.dirname(__file__), "default_theme.json")

default_theme = {
    "background": "#121212",
    "text_color": "#FFFFFF",
    "button_color": "#1E88E5",
    "border_radius": "5px"
}

def load_theme():
    """Loads the theme from a JSON file, or creates a default one if missing."""
    if not os.path.exists(theme_file):
        save_theme(default_theme)

    try:
        with open(theme_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading theme: {e}")
        return default_theme  # Return default if there's an issue

def save_theme(theme):
    """Saves the given theme dictionary to the JSON file."""
    try:
        with open(theme_file, "w", encoding="utf-8") as f:
            json.dump(theme, f, indent=4)
    except IOError as e:
        print(f"Error saving theme: {e}")

if __name__ == "__main__":
    print("Current Theme:", load_theme())
