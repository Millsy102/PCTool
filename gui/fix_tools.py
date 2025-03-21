import psutil
import subprocess
import platform
import os
import csv
import time
import json
import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QLineEdit, QLabel, QTabWidget, QTreeWidget, QTreeWidgetItem, QComboBox, QFileDialog, QProgressBar, QHBoxLayout,
    QCheckBox, QDialog, QTextEdit, QSpinBox, QInputDialog
)
from PyQt6.QtCore import QTimer, Qt

# Configure logging
logging.basicConfig(filename="process_monitor.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

class ProcessesTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.process_list_tab = QWidget()
        self.process_list_layout = QVBoxLayout()
        self.process_list_tab.setLayout(self.process_list_layout)
        self.tabs.addTab(self.process_list_tab, "Process List")

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by name or PID...")
        self.search_bar.textChanged.connect(self.list_processes)
        self.process_list_layout.addWidget(self.search_bar)

        self.process_table = QTableWidget()
        self.process_table.setColumnCount(11)
        self.process_table.setHorizontalHeaderLabels(
            ["PID", "Name", "CPU (%)", "Memory (MB)", "Status", "Threads", "Disk (MB/s)", "Net (KB/s)", "User", "Priority", "Executable Path"]
        )
        self.process_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.process_table.setSortingEnabled(True)
        self.process_list_layout.addWidget(self.process_table)

        self.cpu_progress = QProgressBar()
        self.cpu_progress.setFormat("CPU Usage: %p%")
        self.process_list_layout.addWidget(self.cpu_progress)

        self.ram_progress = QProgressBar()
        self.ram_progress.setFormat("RAM Usage: %p%")
        self.process_list_layout.addWidget(self.ram_progress)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_button("Refresh", self.list_processes))
        button_layout.addWidget(self.create_button("Kill Process", self.kill_selected_process))
        button_layout.addWidget(self.create_button("Suspend", self.suspend_process))
        button_layout.addWidget(self.create_button("Resume", self.resume_process))
        button_layout.addWidget(self.create_button("Set Priority", self.set_process_priority))
        button_layout.addWidget(self.create_button("View Details", self.view_process_details))
        button_layout.addWidget(self.create_button("Export", self.export_report))
        self.process_list_layout.addLayout(button_layout)

        self.dark_mode_toggle = QCheckBox("Dark Mode")
        self.dark_mode_toggle.stateChanged.connect(self.toggle_dark_mode)
        self.process_list_layout.addWidget(self.dark_mode_toggle)

        self.auto_refresh_toggle = QCheckBox("Auto Refresh")
        self.auto_refresh_toggle.setChecked(True)
        self.process_list_layout.addWidget(self.auto_refresh_toggle)

        self.refresh_rate_spinner = QSpinBox()
        self.refresh_rate_spinner.setRange(500, 5000)
        self.refresh_rate_spinner.setValue(2000)
        self.process_list_layout.addWidget(QLabel("Refresh Rate (ms):"))
        self.process_list_layout.addWidget(self.refresh_rate_spinner)

        self.list_processes()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_real_time_stats)
        self.timer.start(self.refresh_rate_spinner.value())
        self.refresh_rate_spinner.valueChanged.connect(self.update_timer_interval)

    def create_button(self, text, function):
        button = QPushButton(text)
        button.clicked.connect(function)
        return button

    def kill_selected_process(self):
        selected_row = self.process_table.currentRow()
        if selected_row >= 0:
            pid = int(self.process_table.item(selected_row, 0).text())
            confirm = QMessageBox.question(self, "Kill Process", f"Are you sure you want to kill process {pid}?", 
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                try:
                    psutil.Process(pid).terminate()
                    logging.info(f"Process {pid} terminated successfully.")
                    QMessageBox.information(self, "Success", "Process terminated successfully.")
                    self.list_processes()
                except Exception as e:
                    logging.error(f"Error terminating process {pid}: {str(e)}")
                    QMessageBox.warning(self, "Error", f"Could not terminate process: {str(e)}")

    def update_real_time_stats(self):
        if self.auto_refresh_toggle.isChecked():
            self.list_processes()
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        self.cpu_progress.setValue(int(cpu_usage))
        self.ram_progress.setValue(int(ram_usage))

    def update_timer_interval(self):
        self.timer.setInterval(self.refresh_rate_spinner.value())

    def set_process_priority(self):
        selected_row = self.process_table.currentRow()
        if selected_row >= 0:
            pid = int(self.process_table.item(selected_row, 0).text())
            priority, ok = QInputDialog.getInt(self, "Set Priority", "Enter priority (-20 to 19):", 0, -20, 19)
            if ok:
                try:
                    psutil.Process(pid).nice(priority)
                    logging.info(f"Priority of process {pid} set to {priority}.")
                    QMessageBox.information(self, "Success", "Process priority updated.")
                except Exception as e:
                    logging.error(f"Error setting priority for process {pid}: {str(e)}")
                    QMessageBox.warning(self, "Error", f"Could not set priority: {str(e)}")

    def view_process_details(self):
        selected_row = self.process_table.currentRow()
        if selected_row >= 0:
            pid = int(self.process_table.item(selected_row, 0).text())
            try:
                process = psutil.Process(pid)
                details = f"Name: {process.name()}\nPath: {process.exe()}\nThreads: {process.num_threads()}\nMemory: {process.memory_info().rss / 1024**2:.2f} MB\nUser: {process.username()}"
                logging.info(f"Viewed details for process {pid}.")
                QMessageBox.information(self, "Process Details", details)
            except Exception as e:
                logging.error(f"Error fetching details for process {pid}: {str(e)}")
                QMessageBox.warning(self, "Error", f"Could not fetch details: {str(e)}")

    def toggle_dark_mode(self):
        self.setStyleSheet("background-color: #2e2e2e; color: white;" if self.dark_mode_toggle.isChecked() else "")
