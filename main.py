import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt6.QtGui import QIcon

# Add the core directory to the system path
sys.path.append(r'C:\Users\Robert\Desktop\Project\core')

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
        self.setWindowIcon(QIcon("assets/icon.png"))

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
