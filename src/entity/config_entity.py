
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

@dataclass
class ModelTrainingConfig:
    model_training_dir : str = os.path.join(training_pipeline_config.artifact_dir,MODEL_DIR_NAME)
    model_training_dir_name : str = os.path.join(model_training_dir,MODEL_NAME)

    model  = MODEL

@dataclass
class ModelEvaluationConfig:
    model_evaluation_dir : str = os.path.join(training_pipeline_config.artifact_dir, MODEL_EVALUATION_DIR)
    model_evaluation_dir_name : str = os.path.join(model_evaluation_dir,MODEL_EVALUATION_DIR_NAME)
    expected_accuracy : float = ACCURACY_THRESHOLD

@dataclass
class ModelPusherConfig:
    model_pusher_dir: str = os.path.join(training_pipeline_config.artifact_dir, MODEL_PUSHER_DIR_NAME)
    saved_model_dir: str = SAVED_MODEL_DIR
    saved_model_path: str = os.path.join(SAVED_MODEL_DIR, MODEL_NAME)