# log_utils.py
import logging
import os
from datetime import datetime

def setup_logging():
    # Get the current day of the week
    day_of_week = datetime.now().strftime("%A")
    # Create a logs directory path based on the current day
    logs_directory = os.path.join(os.getcwd(), 'logs', day_of_week)
    
    # Create the logs directory if it doesn't exist
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    # Create a log file name based on the current date and time
    log_file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
    log_file_path = os.path.join(logs_directory, log_file_name)
    
    # Set up the basic configuration for logging
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Log that the file was initialized
    logger = logging.getLogger()
    logger.info("Log file initialized.")
    return logger
