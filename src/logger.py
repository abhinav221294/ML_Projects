import logging
import os
from datetime import datetime

# Create a log file name using the current date and time
# Example: "10_26_2025_14_35_12.log"
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Define only the logs directory path
log_dir = os.path.join(os.getcwd(), "logs")

# Create the 'logs' directory if it doesn’t exist
os.makedirs(log_dir, exist_ok=True)

# Now create the full log file path inside that folder
LOG_FILE_PATH = os.path.join(log_dir, LOG_FILE)

# Configure logging settings
logging.basicConfig(
    filename=LOG_FILE_PATH,  # File where logs will be written
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO       # Capture INFO and above
)