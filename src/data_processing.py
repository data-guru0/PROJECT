import os
import pandas as pd
from config.paths_config import TRAIN_DATA_PATH, ARTIFACTS_DIR
from src.logger import get_logger
from src.custom_exception import CustomException
import sys
logger = get_logger(__name__)

class DataProcessor:
    def __init__(self):
        self.train_data_path = TRAIN_DATA_PATH
        self.processed_data_path = os.path.join(ARTIFACTS_DIR, "processed_data", "processed_train.csv")

    def load_data(self):
        try:
            logger.info(f"Loading data from: {self.train_data_path}")
            df = pd.read_csv(self.train_data_path)
            logger.info(f"Data loaded successfully. Shape: {df.shape}")
            return df
        except Exception as e:
            logger.error("Error while loading data")
            raise CustomException("Error while loading data", e)

    def drop_unnecessary_columns(self, df, columns):
        try:
            logger.info(f"Dropping columns: {columns}")
            df = df.drop(columns=columns, axis=1)
            logger.info(f"Columns dropped successfully. Shape: {df.shape}")
            return df
        except Exception as e:
            logger.error("Error while dropping columns")
            raise CustomException("Error while dropping columns", e)

    def handle_outliers(self, df, columns):
        try:
            logger.info(f"Handling outliers for columns: {columns}")
            for column in columns:
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1

                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                df[column] = df[column].clip(lower=lower_bound, upper=upper_bound)

            logger.info("Outliers handled successfully.")
            return df
        except Exception as e:
            logger.error("Error while handling outliers")
            raise CustomException("Error while handling outliers", e)

    def handle_null_values(self, df, column, strategy="median"):
        try:
            logger.info(f"Handling null values for column: {column} using strategy: {strategy}")
            if strategy == "median":
                df[column] = df[column].fillna(df[column].median())
                logger.info(f"Null values in column '{column}' filled with median.")
            else:
                logger.warning("Currently, only 'median' strategy is implemented.")
            return df
        except Exception as e:
            logger.error("Error while handling null values")
            raise CustomException("Error while handling null values", e)

    def save_data(self, df):
        try:
            output_dir = os.path.dirname(self.processed_data_path)
            os.makedirs(output_dir, exist_ok=True)
            df.to_csv(self.processed_data_path, index=False)
            logger.info(f"Processed data saved at: {self.processed_data_path}")
        except Exception as e:
            logger.error("Error while saving processed data")
            raise CustomException("Error while saving processed data", e)

    def run(self):
        try:
            logger.info("Starting the data processing pipeline.")
            
            # Load the data
            df = self.load_data()

            # Drop unnecessary columns
            df = self.drop_unnecessary_columns(df, columns=["MyUnknownColumn", "id"])

            # Handle outliers
            outlier_columns = [
                "Flight Distance",
                "Departure Delay in Minutes",
                "Arrival Delay in Minutes",
                "Checkin service",
            ]
            df = self.handle_outliers(df, outlier_columns)

            # Handle null values
            df = self.handle_null_values(df, column="Arrival Delay in Minutes", strategy="median")

            # Save the processed data
            self.save_data(df)

            logger.info("Data processing pipeline completed successfully.")
        except CustomException as ce:
            logger.error(f"Pipeline execution failed: {str(ce)}")
        except Exception as e:
            logger.error("An unexpected error occurred")
            raise CustomException("Unexpected error during pipeline execution", e)
        finally:
            logger.info("End of data processing pipeline")


if __name__ == "__main__":
    processor = DataProcessor()
    processor.run()
