import psutil

def get_network_usage():
    net_io = psutil.net_io_counters()
    return {
        "Bytes Sent": net_io.bytes_sent,
        "Bytes Received": net_io.bytes_recv
    }
