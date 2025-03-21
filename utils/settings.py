import json
import os

settings_file = os.path.join(os.path.dirname(__file__), "../config/settings.json")

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
    if not os.path.exists(settings_file):
        save_settings(default_settings)
    with open(settings_file, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(settings_file, "w") as f:
        json.dump(settings, f, indent=4)
