import json
import os

settings_file = os.path.join(os.path.dirname(__file__), "..", "config", "settings.json")

default_settings = {
    "theme": "dark",
    "refresh_rate": 1,
    "alert_thresholds": {
        "cpu": 90,
        "ram": 90,
        "disk": 90
    }
}

def load_settings():
    """Load settings from the JSON file. If the file doesn't exist, create it with default settings."""
    if not os.path.exists(settings_file):
        save_settings(default_settings)

    try:
        with open(settings_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        save_settings(default_settings)
        return default_settings

def save_settings(settings):
    """Save settings to the JSON file."""
    os.makedirs(os.path.dirname(settings_file), exist_ok=True)
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)

if __name__ == "__main__":
    print("Current Settings:", load_settings())
