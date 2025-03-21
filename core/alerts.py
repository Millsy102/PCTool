import psutil

def check_high_usage(cpu_threshold=90, ram_threshold=90, disk_threshold=90):
    alerts = []
    if psutil.cpu_percent() > cpu_threshold:
        alerts.append("⚠ High CPU Usage!")
    if psutil.virtual_memory().percent > ram_threshold:
        alerts.append("⚠ High RAM Usage!")
    if psutil.disk_usage('/').percent > disk_threshold:
        alerts.append("⚠ High Disk Usage!")
    return alerts
