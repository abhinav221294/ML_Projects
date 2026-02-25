# Importing logging module to track events, errors, and information
import logging

# Importing os module to work with file paths and directories
import os

# Importing datetime to generate timestamp-based log file names
from datetime import datetime


# Creating a log file name using current date and time
# strftime formats date into: Month_Day_Year_Hour_Minute_Second
# Example: 02_25_2026_19_45_30.log
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"


# Creating a full path for logs directory:
# os.getcwd() -> current working directory
# "logs" -> folder name
# LOG_FILE -> log file name
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)


# Creating directories if they do not already exist
# exist_ok=True prevents error if folder already exists
os.makedirs(logs_path, exist_ok=True)


# Creating full path for the log file
# This joins:
# logs_path (folder path)
# LOG_FILE (file name)
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)


# Configuring logging system
logging.basicConfig(

    # File where logs will be stored
    filename=LOG_FILE_PATH,

    # Format of each log message:
    # %(asctime)s -> timestamp
    # %(lineno)d  -> line number where logging is called
    # %(name)s    -> module name
    # %(levelname)s -> log level (INFO, ERROR, etc.)
    # %(message)s -> actual log message
    format="[%(asctime)s] %(lineno)d %(name)s -%(levelname)s - %(message)s",

    # Minimum logging level
    # INFO means:
    # INFO, WARNING, ERROR, CRITICAL will be logged
    level=logging.INFO,
)


# This block executes only when this file is run directly
if __name__ == "__main__":

    # Writing an INFO level log message into the log file
    logging.info("logging has started!!")