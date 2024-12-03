import os

# Define all file paths in one place
ARTIFACTS_DIR = "./artifacts"
RAW_DATA_PATH = os.path.join(ARTIFACTS_DIR, "raw", "data.csv")
INGESTED_DATA_DIR = os.path.join(ARTIFACTS_DIR, "ingested_data")
TRAIN_DATA_PATH = os.path.join(INGESTED_DATA_DIR, "train.csv")
TEST_DATA_PATH = os.path.join(INGESTED_DATA_DIR, "test.csv")

PROCESSED_DATA_PATH = os.path.join(ARTIFACTS_DIR, "processed_data", "processed_train.csv")

ENGINNERED_DIR = os.path.join(ARTIFACTS_DIR, "engineered_data")
ENGINNERED_DATA = os.path.join(ARTIFACTS_DIR,"engineered_data","final_df.csv")

PARAMS_PATH = os.path.join("./config","params.json")

MODEL_PATH = os.path.join(ARTIFACTS_DIR,"models","trained_model.pkl")
