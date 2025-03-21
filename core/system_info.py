import platform
import psutil
import socket

def get_system_info():
    info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Architecture": platform.architecture()[0],
        "Processor": platform.processor(),
        "RAM": f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB",
        "Hostname": socket.gethostname(),
        "IP Address": socket.gethostbyname(socket.gethostname())
    }
    return info
