import sys
import os
import psutil
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import QTimer

# Add the core directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from core.utils.logger import get_logger

class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        self.logger = get_logger("Dashboard")
        self.logger.info("Dashboard initialized")
        
        # Create the layout
        layout = QVBoxLayout()

        # Add label to display "Dashboard Overview"
        self.dashboard_label = QLabel("Dashboard Overview")
        layout.addWidget(self.dashboard_label)
        
        # Create layout for displaying system stats
        self.stats_layout = QVBoxLayout()

        # Labels for system information
        self.cpu_label = QLabel("CPU Usage: 0%")
        self.ram_label = QLabel("RAM Usage: 0%")
        self.disk_label = QLabel("Disk Usage: 0%")
        self.network_label = QLabel("Network: 0KB/s")
        
        self.stats_layout.addWidget(self.cpu_label)
        self.stats_layout.addWidget(self.ram_label)
        self.stats_layout.addWidget(self.disk_label)
        self.stats_layout.addWidget(self.network_label)

        # Add stats layout to the main layout
        layout.addLayout(self.stats_layout)

        # Create the refresh button
        refresh_button = QPushButton("Refresh Data")
        refresh_button.clicked.connect(self.refresh_data)
        layout.addWidget(refresh_button)

        # Set the main layout
        self.setLayout(layout)

        # Set up the timer to auto-refresh every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_data)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)
    
    def refresh_data(self):
        """Method to refresh and update system stats."""
        self.logger.info("Refreshing dashboard data...")
        
        # Update CPU, RAM, Disk, and Network stats
        self.cpu_label.setText(f"CPU Usage: {psutil.cpu_percent()}%")
        self.ram_label.setText(f"RAM Usage: {psutil.virtual_memory().percent}%")
        self.disk_label.setText(f"Disk Usage: {psutil.disk_usage('/').percent}%")
        
        # Network stats (in KB/s)
        net_io = psutil.net_io_counters()
        bytes_received = net_io.bytes_recv
        bytes_sent = net_io.bytes_sent
        self.network_label.setText(f"Network: {((bytes_received + bytes_sent) / 1024):.2f}KB/s")
        
        print("Dashboard data refreshed")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = DashboardTab()
    window.show()
    sys.exit(app.exec())
