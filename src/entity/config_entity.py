
import os
from src.constants import *
from dataclasses import dataclass
from datetime import datetime


TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")


@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = PIPELINE_NAME
    artifact_dir: str = os.path.join(ARTIFACT_DIR, TIMESTAMP)
    timestamp: str = TIMESTAMP


training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()

class DataIngestionConfig:
    data_ingestion_dir : str = os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)
    ##artifact/<timestamp>/data_ingestion/ingested/raw.csv
    
    raw_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, RAW_FILE_NAME)
    collection_name : str = COLLECTION_NAME


@dataclass
class DataValidationConfig:
    data_validation_dir : str = os.path.join(training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME)
    validation_report_file_path: str = os.path.join(data_validation_dir, DATA_VALIDATION_REPORT_FILE_NAME)


@dataclass
class DataTransformationConfig:
    data_transformation_dir : str = os.path.join(training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME)

    transformed_training_file_path : str = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, TRAIN_TRANSFORMED_FILE_NAME)
    transformed_test_file_path : str = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, TEST_TRANSFORMED_FILE_NAME)
    
    split_date : str = Train_Test_Split_Date


