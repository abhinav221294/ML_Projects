# ===============================
# IMPORTING REQUIRED LIBRARIES
# ===============================

# Standard modules for file handling and system operations
import os  # Used for file path management, directory creation, etc.
import sys  # Used for system-specific functions (like passing exception info)

# Custom exception and logger modules (from your own project)
from exception import CustomException  # Custom exception class to provide detailed traceback and error context
from logger import logging  # Custom logger to record information, warnings, and errors throughout execution

# External libraries for data handling and machine learning
import pandas as pd  # Pandas is used for reading, writing, and manipulating tabular data
from sklearn.model_selection import train_test_split  # Splits dataset into training and testing subsets
from dataclasses import dataclass  # Simplifies creation of configuration classes with default attributes

# Importing internal components for further pipeline steps
from components.data_transformation import DataTransformation, DataTransformationConfig  # Handles feature preprocessing
from components.model_trainer import ModelTrainer, ModelTrainerConfig  # Handles model training and evaluation


# ===============================
# CONFIGURATION CLASS
# ===============================

# This dataclass defines and stores configuration values related to data ingestion
@dataclass
class DataIngestionConfig:
    # File path for training data (after splitting)
    train_data_path: str = os.path.join('artifacts', "train.csv")
    # File path for testing data (after splitting)
    test_data_path: str = os.path.join('artifacts', "test.csv")
    # File path for saving the raw dataset (before splitting)
    raw_data_path: str = os.path.join('artifacts', "data.csv")


# ===============================
# DATA INGESTION CLASS
# ===============================

# This class handles all operations related to reading raw data,
# saving it locally, and splitting it into training and testing datasets.
class DataIngestion:
    def __init__(self):
        # Initialize the configuration object
        self.ingestion_config = DataIngestionConfig()

    # Main method that performs the ingestion steps
    def initiate_data_ingestion(self):
        # Log the entry point of the ingestion process
        logging.info("Entered the data ingestion method or components")

        try:
            # Step 1: Read raw dataset into a pandas DataFrame
            # (Make sure the file exists at the specified location)
            df = pd.read_csv('src/notebook/data/stud.csv')
            logging.info("Read the dataset as dataframe")  # Log successful data loading

            # Step 2: Create directories for saving raw data (if they don't already exist)
            raw_data_dir = os.path.dirname(self.ingestion_config.raw_data_path)
            
            if not os.path.exists(raw_data_dir):
                os.makedirs(raw_data_dir)  # Create the 'artifacts' folder if missing

            # Step 3: Save the raw dataset to CSV in the artifacts directory
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train test split initiated")  # Log the start of the train-test split process

            # Step 4: Split dataset into train (80%) and test (20%)
            # random_state ensures reproducibility
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Step 5: Save the resulting train and test sets into CSV files
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the data is completed")  # Log successful completion

            # Step 6: Return paths to the created files
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
                # self.ingestion_config.raw_data_path  # optional, currently commented out
            )

        except Exception as e:
            # If any step fails, wrap the error in a CustomException for better debugging
            raise CustomException(e, sys)


# ===============================
# MAIN EXECUTION BLOCK
# ===============================

# This section only runs when the script is executed directly (not imported)
if __name__ == "__main__":
    # Optional: Uncomment to print the path of the OS module being used
    # print(os.__file__)

    # Step 1: Instantiate the DataIngestion class
    obj = DataIngestion()

    # Step 2: Call the data ingestion process to get training and testing file paths
    train_data, test_data = obj.initiate_data_ingestion()

    # Step 3: Initialize Data Transformation stage
    # This will preprocess both the train and test datasets (handle missing values, encode categories, scale numbers)
    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(
        train_path=train_data,
        test_path=test_data
    )

    # Step 4: Initialize Model Trainer stage
    # This stage will train ML models (e.g., Linear Regression, Random Forest, etc.)
    modeltrainer = ModelTrainer()

    # Step 5: Start the model training process using transformed data
    # The model training class will train multiple models, evaluate them, and print the best score
    print(modeltrainer.inititate_model_trainer(train_arr, test_arr))
