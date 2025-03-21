import logging
import os

LOG_FILE = "core/logs/system.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def get_logger(name):
    """Returns a logger instance."""
    return logging.getLogger(name)

if __name__ == "__main__":
    logger = get_logger("TestLogger")
    logger.info("Logger is set up and running.")
