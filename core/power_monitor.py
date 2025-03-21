import psutil

def get_battery_status():
    if hasattr(psutil, "sensors_battery"):
        battery = psutil.sensors_battery()
        if battery:
            return {"percent": battery.percent, "plugged_in": battery.power_plugged}
    return "Battery monitoring not supported."
