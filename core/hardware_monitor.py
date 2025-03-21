import psutil

def get_temperatures():
    if hasattr(psutil, "sensors_temperatures"):
        return psutil.sensors_temperatures()
    return "Temperature monitoring not supported."

def get_fan_speeds():
    if hasattr(psutil, "sensors_fans"):
        return psutil.sensors_fans()
    return "Fan speed monitoring not supported."
