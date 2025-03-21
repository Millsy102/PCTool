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
    if not os.path.exists(theme_file):
        save_theme(default_theme)
    with open(theme_file, "r") as f:
        return json.load(f)

def save_theme(theme):
    with open(theme_file, "w") as f:
        json.dump(theme, f, indent=4)

if __name__ == "__main__":
    print("Current Theme:", load_theme())
