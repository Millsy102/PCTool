import psutil
import subprocess
import platform
import os
import csv
import time
import json
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QLineEdit, QLabel, QTabWidget, QProgressBar, QHBoxLayout,
    QCheckBox, QFileDialog, QSpinBox, QInputDialog
)
from PyQt6.QtCore import QTimer, Qt


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
        self.process_table.setColumnCount(10)
        self.process_table.setHorizontalHeaderLabels(
            ["PID", "Name", "CPU (%)", "Memory (MB)", "Status", "Threads", "Disk (MB/s)", "Net (KB/s)", "User", "Priority"]
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
        button_layout.addWidget(self.create_button("Set Priority", self.set_process_priority))
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

    def list_processes(self):
        search_text = self.search_bar.text().lower()
        self.process_table.setRowCount(0)
        for proc in psutil.process_iter(attrs=["pid", "name", "cpu_percent", "memory_info", "status", "num_threads", "username"]):
            try:
                pid = str(proc.info["pid"])
                name = proc.info["name"]
                if search_text and search_text not in name.lower() and search_text not in pid:
                    continue
                
                cpu_percent = proc.info["cpu_percent"]
                memory = proc.info["memory_info"].rss / (1024 * 1024)
                status = proc.info["status"]
                threads = proc.info["num_threads"]
                user = proc.info["username"] or "N/A"
                priority = proc.nice()
                disk_usage = 0.0
                net_usage = 0.0

                row = self.process_table.rowCount()
                self.process_table.insertRow(row)
                self.process_table.setItem(row, 0, QTableWidgetItem(pid))
                self.process_table.setItem(row, 1, QTableWidgetItem(name))
                self.process_table.setItem(row, 2, QTableWidgetItem(f"{cpu_percent:.2f}"))
                self.process_table.setItem(row, 3, QTableWidgetItem(f"{memory:.2f}"))
                self.process_table.setItem(row, 4, QTableWidgetItem(status))
                self.process_table.setItem(row, 5, QTableWidgetItem(str(threads)))
                self.process_table.setItem(row, 6, QTableWidgetItem(f"{disk_usage:.2f}"))
                self.process_table.setItem(row, 7, QTableWidgetItem(f"{net_usage:.2f}"))
                self.process_table.setItem(row, 8, QTableWidgetItem(user))
                self.process_table.setItem(row, 9, QTableWidgetItem(str(priority)))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

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
                    QMessageBox.information(self, "Success", "Process priority updated.")
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Could not set priority: {str(e)}")

    def export_report(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "CSV Files (*.csv);;JSON Files (*.json)")
        if filename:
            with open(filename, "w") as file:
                json.dump([{col: self.process_table.item(row, col).text() for col in range(self.process_table.columnCount())} for row in range(self.process_table.rowCount())], file, indent=4)
            QMessageBox.information(self, "Success", "Report exported successfully.")

    def toggle_dark_mode(self):
        self.setStyleSheet("background-color: #2e2e2e; color: white;" if self.dark_mode_toggle.isChecked() else "")
