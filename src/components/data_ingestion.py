# Importing standard modules for file handling and system operations
import os  # Provides functions for interacting with the operating system (e.g., file paths, directories)
import sys  # Provides access to system-specific parameters and functions (used for exception handling)

# Importing custom exception and logger modules
from exception import CustomException  # Custom exception class for detailed error reporting
from logger import logging  # Custom logger to log info, warnings, errors

# Importing external libraries for data handling and machine learning
import pandas as pd  # Pandas is used for data manipulation and analysis
from sklearn.model_selection import train_test_split  # Function to split dataset into train and test sets
from dataclasses import dataclass  # Provides decorator to simplify class creation for storing configuration data

from components.data_transformation import DataTransformation,DataTransformationConfig

# DataIngestionConfig is a dataclass that holds paths for storing dataset files
@dataclass
class DataIngestionConfig:
    # Path where training data will be saved
    train_data_path: str = os.path.join('artifacts', "train.csv")
    # Path where testing data will be saved
    test_data_path: str = os.path.join('artifacts', "test.csv")
    # Path where the raw dataset will be saved
    raw_data_path: str = os.path.join('artifacts', "data.csv")


# Main class responsible for data ingestion operations
class DataIngestion:
    def __init__(self):
        # Initialize ingestion configuration by creating an instance of DataIngestionConfig
        self.ingestion_config = DataIngestionConfig()

    # Method to read raw dataset, save it, and split into train and test sets
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or components")  # Log the start of ingestion

        try:
            # Read the CSV file into a Pandas DataFrame
            # The path here is relative to the project directory
            df = pd.read_csv('src/notebook/data/stud.csv')
            logging.info("Read the dataset as dataframe")  # Log successful read

            # Get the directory where raw data will be saved
            raw_data_dir = os.path.dirname(self.ingestion_config.raw_data_path)
            
            # Create the directory if it does not exist
            if not os.path.exists(raw_data_dir):
                os.makedirs(raw_data_dir)

            # Save the raw dataset as CSV
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train test split initiated")  # Log start of train-test split

            # Split the dataset into training and testing sets (80% train, 20% test)
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Save the training set to CSV
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            # Save the testing set to CSV
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the data is completed")  # Log completion of ingestion

            # Return the paths of train, test, and raw datasets
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
                #self.ingestion_config.raw_data_path
            ) 
        except Exception as e:
            # If any exception occurs, raise a CustomException with detailed info
            raise CustomException(e, sys)


# Main entry point of the script
if __name__ == "__main__":
    # Optionally, you can check which `os` module is being used
    # print(os.__file__)

    # Create an instance of DataIngestion and run the ingestion process
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_path=train_data, test_path=test_data)