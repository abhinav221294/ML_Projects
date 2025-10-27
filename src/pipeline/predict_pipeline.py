# ============================
# 📘 PREDICTION PIPELINE SCRIPT
# ============================

# Importing standard and third-party libraries
import sys  # Used to access system-specific parameters and exception details
import pandas as pd  # Used for data handling and creating input DataFrames
from exception import CustomException  # Custom exception handler for consistent error tracing
from utils import load_object  # Custom function to load saved model/preprocessor objects
import dill  # Library used for serializing and deserializing Python objects (used by utils)

# ======================================
# 🔹 CLASS 1: Prediction Pipeline
# ======================================
class PredictPipeline:
    """
    The PredictPipeline class is responsible for:
    - Loading the trained model and preprocessor from artifacts
    - Applying preprocessing to incoming data
    - Returning predictions
    """

    def __init__(self):
        pass  # No initialization required here

    def predict(self, features):
        """
        Predicts the target (e.g., student's math score) based on input features.

        Parameters:
            features (pd.DataFrame): Input data with same columns as training features.

        Returns:
            np.ndarray: Predicted target values.
        """
        try:
            # Paths where the trained model and preprocessor are stored
            model_path = 'artifacts/model.pkl'
            preprocessor_path = 'artifacts/preprocessor.pkl'  # ✅ corrected forward slashes

            # Load the saved model and preprocessor
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)

            # Apply the same preprocessing transformations used during training
            data_scaled = preprocessor.transform(features)

            # Generate predictions using the trained model
            preds = model.predict(data_scaled)

            # Return predictions
            return preds

        except Exception as e:
            # Handle any exception with a detailed traceback
            raise CustomException(e, sys)


# ======================================
# 🔹 CLASS 2: Custom Data
# ======================================
class CustomData:
    """
    Represents a single input data instance for prediction.
    Converts user input into a DataFrame format for model inference.
    """

    def __init__(self,
                 gender: str,
                 race_ethnicity: str,
                 parental_level_of_education: str,
                 lunch: str,
                 test_preparation_course: str,
                 reading_score: int,
                 writing_score: int):
        """
        Initialize user inputs as attributes.
        """
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score

    def get_data_as_data_frame(self):
        """
        Converts the user inputs into a pandas DataFrame,
        ensuring consistency with the model's expected input format.

        Returns:
            pd.DataFrame: DataFrame containing a single row of input data.
        """
        try:
            # Construct dictionary of user-provided input data
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }

            # Convert dictionary to a pandas DataFrame
            df = pd.DataFrame(custom_data_input_dict)
            return df

        except Exception as e:
            raise CustomException(e, sys)


# ======================================
# 🔹 Example Usage (for testing only)
# ======================================
if __name__ == "__main__":
    try:
        # Example input — single student data
        custom_data = CustomData(
            gender="female",
            race_ethnicity="group B",
            parental_level_of_education="bachelor's degree",
            lunch="standard",
            test_preparation_course="completed",
            reading_score=72,
            writing_score=74
        )

        # Convert to DataFrame
        input_df = custom_data.get_data_as_data_frame()
        print("Input DataFrame:\n", input_df)

        # Create pipeline object and make prediction
        predict_pipeline = PredictPipeline()
        prediction = predict_pipeline.predict(input_df)

        print("\nPredicted Math Score:", prediction)

    except Exception as e:
        raise CustomException(e, sys)
