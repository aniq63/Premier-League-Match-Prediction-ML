import os
from datetime import datetime


# Database MONGO DB constants
MONGODB_URL_KEY = "MONGODB_URL"
DATABASE_NAME = "Soccer-Data"
COLLECTION_NAME = "PremierLeague-Matches-Data"


PIPELINE_NAME: str = ""
ARTIFACT_DIR: str = "artifact"

FILE_NAME: str = "data.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"


# Data ingestion constants
DATA_INGESTION_COLLECTION_NAME: str = "PremierLeague-Matches-Data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
Train_Test_Split_Date = '2025-12-10'