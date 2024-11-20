import os
import csv
import mysql.connector
from mysql.connector import Error
from config.db_config import DB_CONFIG
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)


class MySQLDataExtractor:
    """
    A class to extract data from a MySQL database table and save it as a CSV file.
    """

    def __init__(self, db_config):
        """
        Initialize the database connection parameters.

        Parameters:
            db_config (dict): Database configuration dictionary with keys: host, user, password, database, table_name.
        """
        self.host = db_config["host"]
        self.user = db_config["user"]
        self.password = db_config["password"]
        self.database = db_config["database"]
        self.table_name = db_config["table_name"]
        self.connection = None
        logger.info("MySQLDataExtractor initialized with provided database configuration.")

    def connect(self):
        """Establish a connection to the MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                logger.info(f"Successfully connected to the database: {self.database}")
        except Error as e:
            raise CustomException(f"Error connecting to the database: {e}")

    def disconnect(self):
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Database connection closed.")

    def extract_to_csv(self, output_folder="./artifacts/raw"):
        """
        Extract data from the MySQL table and save it as a CSV file.

        Parameters:
            output_folder (str): Path to the folder where the CSV file will be saved. Default is './artifacts/raw'.
        """
        try:
            # Ensure connection is established
            if not self.connection or not self.connection.is_connected():
                self.connect()

            # Fetch data
            cursor = self.connection.cursor()
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            logger.info("Data fetched successfully from the database.")

            # Ensure output folder exists
            os.makedirs(output_folder, exist_ok=True)
            csv_file_path = os.path.join(output_folder, "data.csv")

            # Write to CSV
            with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(columns)  # Write header
                writer.writerows(rows)   # Write data
            logger.info(f"Data successfully saved to {csv_file_path}")

        except Error as e:
            raise CustomException(f"Error while extracting data: {e}")

        except CustomException as ce:
            logger.error(str(ce))

        finally:
            if 'cursor' in locals():
                cursor.close()
            self.disconnect()


# Object Creation and Execution
try:
    extractor = MySQLDataExtractor(DB_CONFIG)
    extractor.extract_to_csv()
except CustomException as ce:
    logger.error(str(ce))
