import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt6.QtGui import QIcon
from .dashboard import DashboardTab
from .processes import ProcessesTab
from .fix_tools import FixToolsTab
from .settings import SettingsTab

class SystemMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Monitor")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon("icon.png"))

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.dashboard_tab = DashboardTab()
        self.process_tab = ProcessesTab()
        self.fix_tools_tab = FixToolsTab()
        self.settings_tab = SettingsTab()

        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        self.tabs.addTab(self.process_tab, "Processes")
        self.tabs.addTab(self.fix_tools_tab, "Fix Tools")
        self.tabs.addTab(self.settings_tab, "Settings")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemMonitor()
    window.show()
    sys.exit(app.exec())
