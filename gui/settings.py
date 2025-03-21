import os
import json
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QLineEdit, QLabel, QCheckBox, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt


class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        # File Picker Button to select a configuration file
        self.file_picker = QPushButton("Select Config File")
        self.file_picker.clicked.connect(self.open_settings)
        layout.addWidget(self.file_picker)

        # Settings Controls
        self.theme_label = QLabel("Select Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "Futuristic"])
        layout.addWidget(self.theme_label)
        layout.addWidget(self.theme_combo)

        self.language_label = QLabel("Select Language:")
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Spanish", "French"])
        layout.addWidget(self.language_label)
        layout.addWidget(self.language_combo)

        self.enable_notifications = QCheckBox("Enable Notifications")
        layout.addWidget(self.enable_notifications)

        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load Settings")
        self.load_button.clicked.connect(self.load_settings)
        layout.addWidget(self.load_button)

        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)

        self.current_config = {}
        self.default_config_path = "config.json"

    def open_settings(self):
        """Open the configuration file and load its content."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Configuration File", "", "Config Files (*.json)")
        if file_path:
            self.load_settings(file_path)

    def load_settings(self, file_path=None):
        """Load settings from a config file."""
        file_path = file_path or self.default_config_path

        if not os.path.exists(file_path):
            QMessageBox.warning(self, "Error", f"Configuration file not found: {file_path}")
            self.status_label.setText("Failed to load settings.")
            return

        try:
            with open(file_path, "r", encoding="utf-8") as config_file:
                self.current_config = json.load(config_file)

            # Set UI elements based on loaded settings
            self.theme_combo.setCurrentText(self.current_config.get("theme", "Light"))
            self.language_combo.setCurrentText(self.current_config.get("language", "English"))
            self.enable_notifications.setChecked(self.current_config.get("enable_notifications", False))
            self.status_label.setText(f"Settings Loaded from {file_path}")

        except json.JSONDecodeError:
            QMessageBox.warning(self, "Error", "Invalid JSON format in the settings file.")
            self.status_label.setText("Failed to load settings.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not load settings: {e}")
            self.status_label.setText("Failed to load settings.")

    def save_settings(self):
        """Save current settings to a config file."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Configuration File", "", "Config Files (*.json)")
        if not file_path:
            return  # User canceled

        try:
            settings_data = {
                "theme": self.theme_combo.currentText(),
                "language": self.language_combo.currentText(),
                "enable_notifications": self.enable_notifications.isChecked(),
            }

            with open(file_path, "w", encoding="utf-8") as config_file:
                json.dump(settings_data, config_file, indent=4)

            self.status_label.setText(f"Settings saved to {file_path}")
            QMessageBox.information(self, "Success", "Settings saved successfully.")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not save settings: {e}")
            self.status_label.setText("Failed to save settings.")
