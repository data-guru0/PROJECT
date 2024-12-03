import os
import pandas as pd
import sys
import joblib
import json
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import lightgbm as lgb
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *

# Initialize logger
logger = get_logger(__name__)

class ModelTraining:
    def __init__(self, data_path, params_path, model_save_path, experiment_name="Model_Training_Experiment"):
        """
        Initializes the ModelTraining class.
        Args:
            data_path (str): Path to the data CSV file.
            params_path (str): Path to the JSON file containing hyperparameters.
            model_save_path (str): Path to save the trained model.
            experiment_name (str): Name of the MLflow experiment.
        """
        self.data_path = data_path
        self.params_path = params_path
        self.model_save_path = model_save_path
        self.best_model = None
        self.metrics = None
        self.experiment_name = experiment_name

    def load_data(self):
        """Loads the dataset."""
        try:
            logger.info(f"Loading data from {self.data_path}")
            data = pd.read_csv(self.data_path)
            logger.info("Data loaded successfully")
            return data
        except Exception as e:
            raise CustomException("Error loading data", sys)

    def train_model(self, X_train, y_train, params):
        """Trains the model with hyperparameter tuning."""
        try:
            logger.info("Starting model training with hyperparameter tuning")
            lgbm = lgb.LGBMClassifier()
            grid_search = GridSearchCV(lgbm, param_grid=params, cv=3, scoring='accuracy')
            grid_search.fit(X_train, y_train)
            logger.info("Model training completed")
            self.best_model = grid_search.best_estimator_
            return grid_search.best_params_
        except Exception as e:
            raise CustomException("Error during model training", sys)

    def evaluate_model(self, X_test, y_test):
        """Evaluates the model and logs performance metrics."""
        try:
            logger.info("Evaluating the model")
            y_pred = self.best_model.predict(X_test)
            self.metrics = {
                "accuracy": accuracy_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred, average='weighted'),
                "recall": recall_score(y_test, y_pred, average='weighted'),
                "f1_score": f1_score(y_test, y_pred, average='weighted'),
                "confusion_matrix": confusion_matrix(y_test, y_pred).tolist()  # Convert to list for logging
            }
            logger.info(f"Evaluation metrics: {self.metrics}")
            return self.metrics
        except Exception as e:
            raise CustomException("Error during model evaluation", sys)

    def save_model(self):
        """Saves the trained model to the specified path."""
        try:
            logger.info(f"Saving model to {self.model_save_path}")
            os.makedirs(os.path.dirname(self.model_save_path), exist_ok=True)
            joblib.dump(self.best_model, self.model_save_path)
            logger.info("Model saved successfully")
        except Exception as e:
            raise CustomException("Error saving model", sys)

    def run(self):
        """Executes the complete workflow of loading data, training, evaluating, and saving the model."""
        try:
            # Set up MLflow experiment
            mlflow.set_experiment(self.experiment_name)

            with mlflow.start_run():
                # Load the dataset
                data = self.load_data()

                # Prepare features and target
                X = data.drop(columns='satisfaction')
                y = data['satisfaction']
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                logger.info("Data split into training and testing sets")

                # Load hyperparameters
                with open(self.params_path, 'r') as f:
                    params = json.load(f)
                logger.info(f"Loaded hyperparameters: {params}")
                
                # Log initial parameters with unique keys
                mlflow.log_params({f"grid_{key}": value for key, value in params.items()})

                # Train the model
                best_params = self.train_model(X_train, y_train, params)
                logger.info(f"Best parameters from tuning: {best_params}")
                mlflow.log_params({f"best_{key}": value for key, value in best_params.items()})  # Log best parameters

                # Evaluate the model
                metrics = self.evaluate_model(X_test, y_test)
                for metric, value in metrics.items():
                    if metric != "confusion_matrix":
                        mlflow.log_metric(metric, value)  # Log metrics

                # Save and log the model
                self.save_model()
                mlflow.sklearn.log_model(self.best_model, "model")  # Log the model

        except CustomException as ce:
            logger.error(str(ce))
            mlflow.end_run(status="FAILED")
        except Exception as e:
            logger.error("An unexpected error occurred during the training process")
            mlflow.end_run(status="FAILED")
            raise CustomException("Unexpected error in the training workflow", sys)


if __name__ == "__main__":
    # Initialize and run the training process
    model_trainer = ModelTraining(
        data_path=ENGINNERED_DATA,
        params_path=PARAMS_PATH,
        model_save_path=MODEL_PATH
    )
    model_trainer.run()
