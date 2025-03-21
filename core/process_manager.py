import psutil

def list_processes():
    processes = []
    for process in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append(process.info)
    return processes

def kill_process(pid):
    try:
        p = psutil.Process(pid)
        p.terminate()
        return f"Process {pid} terminated."
    except Exception as e:
        return str(e)
