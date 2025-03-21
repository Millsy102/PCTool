import logging
import os

log_file = os.path.join(os.path.dirname(__file__), "app.log")

# Configure logging
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_info(message):
    logging.info(message)

def log_warning(message):
    logging.warning(message)

def log_error(message):
    logging.error(message)

if __name__ == "__main__":
    log_info("Logger initialized successfully.")
    print(f"Logging system is set up. Logs will be stored in {log_file}")
