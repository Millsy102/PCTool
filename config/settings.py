import json
import os

CONFIG_FILE = "core/config/settings.json"

def load_config():
    """Loads configuration settings from the JSON file."""
    if not os.path.exists(CONFIG_FILE):
        print("Config file not found! Creating default config...")
        save_default_config()
    
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

def save_default_config():
    """Creates and saves a default configuration file."""
    default_config = {
        "theme": "dark",
        "log_level": "DEBUG",
        "refresh_rate": 1,
        "alerts": {
            "cpu_threshold": 80,
            "ram_threshold": 80,
            "disk_threshold": 90
        }
    }
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w") as file:
        json.dump(default_config, file, indent=4)

def update_config(new_settings):
    """Updates the configuration file with new settings."""
    config = load_config()
    config.update(new_settings)
    
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)
    print("Configuration updated successfully.")

if __name__ == "__main__":
    config = load_config()
    print("Current Configuration:", config)
