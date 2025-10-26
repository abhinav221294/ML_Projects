# Importing essential libraries and modules
import sys  # Used for exception handling and system-level operations
from dataclasses import dataclass  # For creating configuration classes easily

# Data manipulation and ML preprocessing libraries
import numpy as np  # For numerical operations
import pandas as pd  # For handling data in DataFrame format

# Scikit-learn tools for preprocessing
from sklearn.compose import ColumnTransformer  # To apply transformations to specific columns
from sklearn.impute import SimpleImputer  # To fill missing values
from sklearn.pipeline import Pipeline  # To create chained data processing workflows
from sklearn.preprocessing import OneHotEncoder, StandardScaler  # For encoding categorical and scaling numeric data

# Custom imports for logging, exceptions, and utilities
from exception import CustomException  # Custom error handler class
from logger import logging  # Custom logger for tracking execution
import os  # For file path handling
from utils import save_object  # Custom utility function to save Python objects (using pickle)


# Configuration class for data transformation (uses dataclass for cleaner syntax)
@dataclass
class DataTransformationConfig:
    # File path where the preprocessor object (pickle file) will be saved
    preprocessor_obj_file_path = os.path.join('artifacts', "proprocessor.pkl")


# Main class to handle data transformation tasks
class DataTransformation:
    def __init__(self):
        # Initialize configuration
        self.data_transformation_config = DataTransformationConfig()
        
    # Function to create and return a preprocessing object (ColumnTransformer)
    def get_data_transformer_object(self):
        '''
        This function is responsible for defining and returning 
        the preprocessing pipelines for both numerical and categorical features.
        '''

        try:
            # Define numerical and categorical feature names
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            # Define the numerical pipeline:
            # 1. Handle missing values using median strategy
            # 2. Standardize numerical values
            num_pipeline = Pipeline(
                steps=[
                    ("impyter", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            # Define the categorical pipeline:
            # 1. Handle missing values using most frequent value
            # 2. Apply one-hot encoding to convert categories to numeric form
            cat_pipeline = Pipeline(
                steps=[
                    ("impute", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder())
                ]
            )

            # Logging the progress of encoding and scaling
            logging.info("Categorical columns encoding scaling completed")
            logging.info("Categorical columns encoding completed")

            # Combine both numerical and categorical pipelines into one preprocessor
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipline", cat_pipeline, categorical_columns)
                ]
            )

            # Return the complete preprocessing object
            return preprocessor

        except Exception as e:
            # Handle any error using custom exception
            raise CustomException(e, sys)
         
    
    # Function to apply preprocessing to train and test datasets
    def initiate_data_transformation(self, train_path, test_path):
        try:
            # Read the training and testing datasets from CSV files
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test completed")
            logging.info("Obtaining preprocessing object")

            # Get the preprocessing object (ColumnTransformer)
            preprocessing_obj = self.get_data_transformer_object()

            # Define the target (dependent variable) column
            target_column_name = "math_score"

            # Define feature columns again for clarity
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            # Separate input (features) and output (target) for training data
            input_feature_train_df = train_df.drop(columns=[target_column_name])
            target_feature_train_df = train_df[target_column_name]

            # Separate input (features) and output (target) for testing data
            input_feature_test_df = test_df.drop(columns=[target_column_name])
            target_feature_test_df = test_df[target_column_name]
            
            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe"
            )

            # Apply the preprocessing object:
            # Fit and transform the training data (fit learns transformations)
            input_feature_train_df_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            # Only transform the test data (without fitting)
            input_feature_test_df_arr = preprocessing_obj.transform(input_feature_test_df)

            # Combine transformed input features with the target column (for train and test)
            train_arr = np.c_[
                input_feature_train_df_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_df_arr, np.array(target_feature_test_df)
            ]
            
            logging.info(f"Saved preprocessing object.")

            # Save the preprocessing object to disk for future use (e.g., during model inference)
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            # Return the transformed training data, test data, and path to the saved preprocessor
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            # Handle and raise any exceptions during transformation
            raise CustomException(e, sys)
