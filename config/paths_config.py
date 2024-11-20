import os

# Define all file paths in one place
ARTIFACTS_DIR = "./artifacts"
RAW_DATA_PATH = os.path.join(ARTIFACTS_DIR, "raw", "data.csv")
INGESTED_DATA_DIR = os.path.join(ARTIFACTS_DIR, "ingested_data")
TRAIN_DATA_PATH = os.path.join(INGESTED_DATA_DIR, "train.csv")
TEST_DATA_PATH = os.path.join(INGESTED_DATA_DIR, "test.csv")
