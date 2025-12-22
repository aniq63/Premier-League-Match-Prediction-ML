import os
from datetime import datetime
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier


# Database MONGO DB constants
MONGODB_URL_KEY = "MONGODB_URL"
DATABASE_NAME = "Soccer-Data"
COLLECTION_NAME = "PremierLeague-Matches-Data"


PIPELINE_NAME: str = ""
ARTIFACT_DIR: str = "artifact"

RAW_FILE_NAME: str = "raw.csv"
TRAIN_TRANSFORMED_FILE_NAME: str = "train.csv"
TEST_TRANSFORMED_FILE_NAME: str = "test.csv"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")
MODEL_NAME = 'model.pkl'


# Data ingestion constants
DATA_INGESTION_COLLECTION_NAME: str = "PremierLeague-Matches-Data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"

# Train Test Split constants
Train_Test_Split_Date = '2025-12-10'


# Data Validation constansts
DATA_VALIDATION_DIR_NAME = 'data_validation'
DATA_VALIDATION_REPORT_FILE_NAME: str = "report.yaml"

# Data Tansformation constants
DATA_TRANSFORMATION_DIR_NAME = 'data_transformation'
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"

# Model Training constants
MODEL_DIR_NAME = 'model_training'
# Model Parameter
BASE_ESTIMATOR = DecisionTreeClassifier(
    max_depth=2,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42
)

MODEL = AdaBoostClassifier(
    estimator=BASE_ESTIMATOR,
    n_estimators=200,
    learning_rate=0.1,
    random_state=42
)

# Model Evaluation constsnts
MODEL_EVALUATION_DIR = 'model_evaluation'
MODEL_EVALUATION_DIR_NAME = 'report'
ACCURACY_THRESHOLD :float = 0.65

# Model Pusher constants
MODEL_PUSHER_DIR_NAME = 'model_pusher'
SAVED_MODEL_DIR = 'saved_models'




