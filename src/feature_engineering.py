import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import mutual_info_classif
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import ARTIFACTS_DIR
from utils.helpers import label_encode

# Setting up logger
logger = get_logger(__name__)

class FeatureEngineer:
    def __init__(self):
        self.data_path = os.path.join(ARTIFACTS_DIR, "processed_data", "processed_train.csv")
        self.df = None
        self.label_mappings = {}

    # Method to load data
    def load_data(self):
        try:
            logger.info(f"Loading data from {self.data_path}")
            self.df = pd.read_csv(self.data_path)
            logger.info(f"Data loaded successfully with shape: {self.df.shape}")
        except Exception as e:
            logger.error(f"Error while loading data: {e}")
            raise CustomException("Error while loading data", e)

    # Method for Feature Construction
    def feature_construction(self):
        try:
            logger.info("Performing feature construction.")
            self.df['Total Delay'] = self.df['Departure Delay in Minutes'] + self.df['Arrival Delay in Minutes']
            self.df['Delay Ratio'] = self.df['Total Delay'] / (self.df['Flight Distance'] + 1)
            logger.info("Feature construction completed successfully.")
        except Exception as e:
            logger.error(f"Error during feature construction: {e}")
            raise CustomException("Error during feature construction", e)

    # Method for Binning Age
    def bin_age(self):
        try:
            logger.info("Binning Age values.")
            self.df['Age Group'] = pd.cut(self.df['Age'], bins=[0, 18, 30, 50, 100], labels=['Child', 'Youngster', 'Adult', 'Senior'])
            logger.info("Age binning completed successfully.")
        except Exception as e:
            logger.error(f"Error during binning age: {e}")
            raise CustomException("Error during binning age", e)

    # Method for Label Encoding
    def label_encoding(self):
        try:
            columns_to_encode = ['Gender', 'Customer Type', 'Type of Travel', 'Class', 'satisfaction', 'Age Group']
            logger.info(f"Performing label encoding for columns: {columns_to_encode}")
            self.df, self.label_mappings = label_encode(self.df, columns_to_encode)
            
            # Log encoding mappings
            for col, mapping in self.label_mappings.items():
                logger.info(f"Mapping for {col}: {mapping}")
            logger.info("Label encoding completed successfully.")
        except Exception as e:
            logger.error(f"Error during label encoding: {e}")
            raise CustomException("Error during label encoding", e)

    # Method for Feature Selection
    def feature_selection(self):
        try:
            logger.info("Performing feature selection using Mutual Information.")
            X = self.df.drop(columns='satisfaction')
            y = self.df['satisfaction']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Mutual Information
            mutual_info = mutual_info_classif(X_train, y_train, discrete_features=True)
            mutual_info_df = pd.DataFrame({
                'Feature': X.columns,
                'Mutual Information': mutual_info
            }).sort_values(by='Mutual Information', ascending=False)

            logger.info(f"Mutual Information: \n{mutual_info_df}")

            # Selecting top 12 features
            top_features = mutual_info_df.head(12)['Feature'].tolist()
            self.df = self.df[top_features + ['satisfaction']]
            logger.info(f"Final selected features: {top_features}")
        except Exception as e:
            logger.error(f"Error during feature selection: {e}")
            raise CustomException("Error during feature selection", e)

    # Method to save the processed data
    def save_processed_data(self):
        try:
            output_dir = os.path.join(ARTIFACTS_DIR, "enginnered_data")
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, "final_df.csv")
            self.df.to_csv(output_path, index=False)
            logger.info(f"Final dataframe saved at {output_path}")
        except Exception as e:
            logger.error(f"Error while saving processed data: {e}")
            raise CustomException("Error while saving processed data", e)

    # Main pipeline to run the feature engineering
    def run(self):
        try:
            logger.info("Starting the feature engineering process.")
            self.load_data()
            self.feature_construction()
            self.bin_age()
            self.label_encoding()
            self.feature_selection()
            self.save_processed_data()
            logger.info("Feature engineering pipeline completed successfully.")
        except CustomException as ce:
            logger.error(f"Feature engineering execution failed: {str(ce)}")
        except Exception as e:
            logger.error(f"Unexpected error during feature engineering pipeline: {str(e)}")
            raise CustomException("Unexpected error during feature engineering pipeline", e)
        finally:
            logger.info("End of feature engineering pipeline.")

if __name__ == "__main__":
    feature_engineer = FeatureEngineer()
    feature_engineer.run()
