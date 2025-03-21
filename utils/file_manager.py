import os

def list_files(directory):
    if os.path.exists(directory):
        return os.listdir(directory)
    return []

def delete_file(filepath):
    try:
        os.remove(filepath)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except Exception as e:
        print(f"Error deleting file: {e}")
