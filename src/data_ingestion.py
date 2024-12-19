import os
import pandas as pd
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *


logger = get_logger(__name__)

class DataIngestion:
    """
    A class to handle the ingestion of raw data and its splitting into training and testing datasets.
    """

    def __init__(self, raw_data_path, ingested_data_dir):
        """
        Initialize paths for raw data and output directories.

        Parameters:
            raw_data_path (str): Path to the raw data CSV file.
            ingested_data_dir (str): Path to the directory where ingested data will be stored.
        """
        self.raw_data_path = raw_data_path
        self.ingested_data_dir = ingested_data_dir
        logger.info("DataIngestion initialized.")

    def create_ingested_data_dir(self):
        """
        Create the directory for storing ingested data if it doesn't exist.
        """
        try:
            os.makedirs(self.ingested_data_dir, exist_ok=True)
            logger.info(f"Directory created or already exists: {self.ingested_data_dir}")
        except Exception as e:
            raise CustomException(f"Error creating directory {self.ingested_data_dir}: {e}")

    def log_file_size(self, file_path, file_type):
        """
        Log the size of the CSV file in terms of rows and columns.

        Parameters:
            file_path (str): Path to the file.
            file_type (str): Type of file (e.g., 'train' or 'test').
        """
        try:
            data = pd.read_csv(file_path)
            rows, cols = data.shape
            logger.info(f"{file_type.capitalize()} Data: {rows} rows and {cols} columns.")
        except Exception as e:
            raise CustomException(f"Error reading {file_type} file at {file_path} for size logging: {e}")

    def split_data(self, train_path, test_path, test_size=0.2, random_state=42):
        """
        Split the raw data into training and testing datasets.

        Parameters:
            train_path (str): Path to save the training data.
            test_path (str): Path to save the testing data.
            test_size (float): Proportion of the dataset to include in the test split.
            random_state (int): Random state for reproducibility.

        Raises:
            CustomException: If any error occurs during the data split or save process.
        """
        try:
            # Load raw data
            if not os.path.exists(self.raw_data_path):
                raise CustomException(f"Raw data file not found: {self.raw_data_path}")
            
            data = pd.read_csv(self.raw_data_path)
            logger.info("Raw data successfully loaded.")

            # Split the data
            train_data, test_data = train_test_split(data, test_size=test_size, random_state=random_state)
            logger.info("Data successfully split into train and test sets.")

            # Save the split data
            train_data.to_csv(train_path, index=False)
            logger.info(f"Training data saved to {train_path}")
            
            test_data.to_csv(test_path, index=False)
            logger.info(f"Testing data saved to {test_path}")

            # Log file sizes
            self.log_file_size(train_path, "train")
            self.log_file_size(test_path, "test")

        except Exception as e:
            raise CustomException(f"Error during data split and save: {e}")


# Main Execution
if __name__ == "__main__":
    try:
        # Initialize DataIngestion
        ingestion = DataIngestion(raw_data_path=RAW_DATA_PATH, ingested_data_dir=INGESTED_DATA_DIR)

        # Create directory for ingested data
        ingestion.create_ingested_data_dir()

        # Split and save the data
        ingestion.split_data(train_path=TRAIN_DATA_PATH, test_path=TEST_DATA_PATH)

    except CustomException as ce:
        logger.error(str(ce))
