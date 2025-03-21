import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt6.QtGui import QIcon

# Dynamically set the core directory path
CORE_DIR = os.path.join(os.getcwd(), "core")
if CORE_DIR not in sys.path:
    sys.path.append(CORE_DIR)

# Import your modules
from gui.dashboard import DashboardTab
from gui.processes import ProcessesTab
from gui.fix_tools import FixToolsTab
from gui.settings import SettingsTab

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ultimate AI System")
        self.setGeometry(100, 100, 1200, 800)

        # Ensure the icon path is cross-platform compatible
        ICON_PATH = os.path.join(os.getcwd(), "assets", "icon.png")
        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))
        else:
            print(f"Warning: Icon file not found at {ICON_PATH}")

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Create tabs
        self.dashboard_tab = DashboardTab()
        self.process_tab = ProcessesTab()
        self.fix_tools_tab = FixToolsTab()
        self.settings_tab = SettingsTab()

        # Add tabs
        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        self.tabs.addTab(self.process_tab, "Processes")
        self.tabs.addTab(self.fix_tools_tab, "Fix Tools")
        self.tabs.addTab(self.settings_tab, "Settings")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainUI()
    window.show()
    sys.exit(app.exec())
