# Import built-in modules for logging, file handling, and datetime operations
import logging
import os
from datetime import datetime

# Create a log file name based on the current date and time
# Example: "10_26_2025_14_35_12.log"
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Define the folder path where logs will be stored: <current_working_directory>/logs/<LOG_FILE>
# ⚠️ NOTE: os.makedirs should create a directory, not a file. We will fix this below.
log_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

# Create the directory if it doesn't exist
# ⚠️ Here, log_path currently points to a file, so os.makedirs will fail.
os.makedirs(log_path, exist_ok=True)  # This line will raise an error

# Full path for the log file (directory + log file name)
LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)

# Configure the logging settings
logging.basicConfig(
    filename=LOG_FILE_PATH,  # File where logs will be written
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO       # Logging level (INFO and above will be logged)
)
