import os

def list_files(directory):
    if os.path.exists(directory):
        return os.listdir(directory)
    return []

def delete_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        return f"{filepath} deleted."
    return "File not found."
