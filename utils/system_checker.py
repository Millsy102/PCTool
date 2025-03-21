import shutil
import psutil

def check_disk_space():
    total, used, free = shutil.disk_usage("/")
    return {"total": total, "used": used, "free": free}

def check_memory():
    mem = psutil.virtual_memory()
    return {"total": mem.total, "used": mem.used, "free": mem.available}
