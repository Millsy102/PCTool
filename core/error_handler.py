import logging

logging.basicConfig(filename='logs/error.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_error(error_message):
    logging.error(error_message)
