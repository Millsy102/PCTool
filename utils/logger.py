import logging
import os

LOG_FILE = os.path.join("core", "logs", "system.log")

# Ensure the logs directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def get_logger(name):
    """Returns a configured logger instance."""
    return logging.getLogger(name)

if __name__ == "__main__":
    logger = get_logger("TestLogger")
    logger.info("Logger is set up and running.")
