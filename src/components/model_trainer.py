# ===========================================
# IMPORTING REQUIRED LIBRARIES AND MODULES
# ===========================================

import os  # Used for file path operations (e.g., saving models)
import sys  # Provides access to system-specific parameters and exception info
from dataclasses import dataclass  # Used for clean configuration classes

# Importing machine learning models and libraries
from catboost import CatBoostRegressor  # Gradient boosting model by Yandex (handles categorical features well)
from sklearn.ensemble import (
    AdaBoostRegressor,  # Boosting algorithm that combines weak learners
    GradientBoostingRegressor,  # Boosting algorithm that sequentially reduces error
    RandomForestRegressor,  # Ensemble of decision trees for regression
)
from sklearn.linear_model import LinearRegression  # Basic linear regression model
from sklearn.metrics import r2_score  # Metric for model evaluation (goodness of fit)
from sklearn.neighbors import KNeighborsRegressor  # KNN model for regression
from sklearn.tree import DecisionTreeRegressor  # Basic decision tree regressor
from xgboost import XGBRegressor  # Popular high-performance gradient boosting model

# Importing project-specific modules for logging, exceptions, and utility functions
from exception import CustomException  # Custom exception handler for better error context
from logger import logging  # Custom logging setup for tracking pipeline stages
from utils import save_object, evaluate_models  # Helper functions for saving objects and evaluating models


# ===========================================
# CONFIGURATION CLASS FOR MODEL TRAINER
# ===========================================

@dataclass
class ModelTrainerConfig:
    # Defines where the final trained model will be saved
    trained_model_file_path = os.path.join("artifacts", "model.pkl")


# ===========================================
# MAIN CLASS FOR MODEL TRAINING
# ===========================================

class ModelTrainer:
    
    def __init__(self):
        # Initialize the configuration class
        self.model_trainer_config = ModelTrainerConfig()
   
    def inititate_model_trainer(self, train_array, test_array):
        """
        This method trains multiple regression models using given train and test data arrays,
        evaluates them, and saves the best-performing model.
        """
        try:
            logging.info("Split training and test input data")

            # ===========================================
            # STEP 1: Split input arrays into features (X) and target (y)
            # ===========================================
            # Assuming the last column is the target variable
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],  # All columns except the last one for training features
                train_array[:, -1],   # Last column for training labels
                test_array[:, :-1],   # All columns except the last one for testing features
                test_array[:, -1]     # Last column for testing labels
            )

            # ===========================================
            # STEP 2: Define a set of candidate regression models
            # ===========================================
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }

            # ===========================================
            # STEP 3: Define hyperparameter grids for tuning each model
            # These parameters will be tested during model evaluation
            # ===========================================
            params = {
                "Decision Tree": {
                    'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                },
                "Random Forest": {
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Gradient Boosting": {
                    'learning_rate': [0.1, 0.01, 0.05, 0.001],
                    'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Linear Regression": {},
                "XGBRegressor": {
                    'learning_rate': [0.1, 0.01, 0.05, 0.001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "CatBoosting Regressor": {
                    'depth': [6, 8, 10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor": {
                    'learning_rate': [0.1, 0.01, 0.5, 0.001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                }
            }

            # ===========================================
            # STEP 4: Evaluate all models using a utility function
            # The evaluate_models() function:
            # - Performs hyperparameter tuning
            # - Fits each model on the training set
            # - Tests each model on the test set
            # - Returns a dictionary of model_name: performance_score
            # ===========================================
            model_report: dict = evaluate_models(
                X_train=X_train, y_train=y_train,
                X_test=X_test, y_test=y_test,
                models=models, param=params
            )

            # ===========================================
            # STEP 5: Identify the best model based on R² score
            # ===========================================
            best_model_score = max(sorted(model_report.values()))  # Highest R² score
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]  # Retrieve model instance

            # ===========================================
            # STEP 6: Validate the best model’s performance threshold
            # If model performance is below 0.6 R², reject all models
            # ===========================================
            if best_model_score < 0.6:
                raise CustomException("No best model found")  # Fail-safe if no good model found

            logging.info("Best model identified successfully")

            # ===========================================
            # STEP 7: Save the best model for future use
            # ===========================================
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            # ===========================================
            # STEP 8: Make predictions on test data using the best model
            # ===========================================
            predicted = best_model.predict(X_test)

            # ===========================================
            # STEP 9: Compute R² score for the best model’s performance
            # ===========================================
            r2_square = r2_score(y_test, predicted)

            # Return the final R² score as the output of this function
            return r2_square

        except Exception as e:
            # Capture any error that occurs and raise as CustomException
            raise CustomException(e, sys)
