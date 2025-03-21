import shutil
import psutil
import platform

def check_disk_space():
    """Returns disk space details in bytes (total, used, free)."""
    try:
        total, used, free = shutil.disk_usage("/")
        return {"total": total, "used": used, "free": free}
    except Exception as e:
        return {"error": str(e)}

def check_memory():
    """Returns memory usage details in bytes (total, used, available)."""
    try:
        mem = psutil.virtual_memory()
        return {"total": mem.total, "used": mem.used, "free": mem.available}
    except Exception as e:
        return {"error": str(e)}

def check_cpu_usage():
    """Returns the current CPU usage percentage."""
    try:
        return {"cpu_usage": psutil.cpu_percent(interval=1)}
    except Exception as e:
        return {"error": str(e)}

def check_system_info():
    """Returns basic system information."""
    try:
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.architecture()[0],
            "processor": platform.processor()
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("Disk Space:", check_disk_space())
    print("Memory:", check_memory())
    print("CPU Usage:", check_cpu_usage())
    print("System Info:", check_system_info())
