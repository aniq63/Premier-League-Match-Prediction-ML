from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTraining
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher

from src.entity.config_entity import (
    DataIngestionConfig, 
    DataValidationConfig, 
    DataTransformationConfig,
    ModelTrainingConfig,
    ModelEvaluationConfig,
    ModelPusherConfig
)
from src.entity.artifact_entity import (
    DataIngestionArtifact, 
    DataValidationArtifact, 
    DataTransformationArtifcat,
    ModelTrainingArtifact,
    ModelEvaluationArtifact,
    ModelPusherArtifact
)
from src.exception import MyException
from src.logger import logging
import sys


class Training_Piepline:
    def __init__(self):
        logging.info("Initializing Training Pipeline")
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_training_config = ModelTrainingConfig()
        self.model_evaluation_config = ModelEvaluationConfig()
        self.model_pusher_config = ModelPusherConfig()

    def Data_Ingestion(self) -> DataIngestionArtifact:
        """
        This method of TrainPipeline class is responsible for starting data ingestion component
        """
        try:
            logging.info("Entered the data_ingestion method of TrainPipeline class")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_DataIngestion()
            logging.info("Got the train_set and test_set from mongodb")
            logging.info("Exited the start_data_ingestion method of TrainPipeline class")
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e, sys) from e
        


    def Data_validation(self, data_ingestion_artifact) -> DataValidationArtifact:
        try:
            logging.info("Entered the data_validation method of TrainPipeline class")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Exited the data_validation method of TrainPipeline class")
            return data_validation_artifact
        except Exception as e:
            raise MyException(e, sys) from e

    def Data_Transformation(self, data_ingestion_artifact, data_validation_artifact) -> DataTransformationArtifcat:
        try:
            logging.info("Entered the data_transformation method of TrainPipeline class")
            data_transformation = DataTransformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validtaion_artifact=data_validation_artifact,
                data_transformation_config=self.data_transformation_config
            )
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Data transformation completed successfully")
            logging.info("Exited the data_transformation method of TrainPipeline class")
            return data_transformation_artifact
        except Exception as e:
            logging.error(f"Error in data transformation: {str(e)}")
            raise MyException(e, sys) from e

    def Model_Training(self, data_transformation_artifact) -> ModelTrainingArtifact:
        try:
            logging.info("Entered the model_training method of TrainPipeline class")
            model_training = ModelTraining(
                data_transformation_artifact=data_transformation_artifact,
                model_training_config=self.model_training_config
            )
            model_training_artifact = model_training.initiate_model_training()
            logging.info("Model training completed successfully")
            logging.info("Exited the model_training method of TrainPipeline class")
            return model_training_artifact
        except Exception as e:
            logging.error(f"Error in model training: {str(e)}")
            raise MyException(e, sys) from e

    def Model_Evaluation(self, model_training_artifact, data_transformation_artifact) -> ModelEvaluationArtifact:
        try:
            logging.info("Entered the model_evaluation method of TrainPipeline class")
            model_evaluation = ModelEvaluation(
                model_training_artifact=model_training_artifact,
                data_transformation_artifact=data_transformation_artifact,
                model_evaluation_config=self.model_evaluation_config
            )
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            logging.info("Model evaluation completed successfully")
            logging.info("Exited the model_evaluation method of TrainPipeline class")
            return model_evaluation_artifact
        except Exception as e:
            logging.error(f"Error in model evaluation: {str(e)}")
            raise MyException(e, sys) from e

    def Model_Pusher(self, model_evaluation_artifact) -> ModelPusherArtifact:
        try:
            logging.info("Entered the model_pusher method of TrainPipeline class")
            model_pusher = ModelPusher(
                model_evaluation_artifact=model_evaluation_artifact,
                model_pusher_config=self.model_pusher_config
            )
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            logging.info("Model pusher completed successfully")
            logging.info("Exited the model_pusher method of TrainPipeline class")
            return model_pusher_artifact
        except Exception as e:
            logging.error(f"Error in model pusher: {str(e)}")
            raise MyException(e, sys) from e

    def run_pipeline(self):
        try:
            logging.info("="*80)
            logging.info("Starting the Complete Training Pipeline")
            logging.info("="*80)
            
            # Step 1: Data Ingestion
            logging.info("\n" + "="*80)
            logging.info("Step 1: Data Ingestion")
            logging.info("="*80)
            data_ingestion_artifact = self.Data_Ingestion()
            logging.info(f"Data Ingestion completed. Train file: {data_ingestion_artifact.trained_file_path}")
            logging.info(f"Test file: {data_ingestion_artifact.test_file_path}")
            
            # Step 2: Data Validation
            logging.info("\n" + "="*80)
            logging.info("Step 2: Data Validation")
            logging.info("="*80)
            data_validation_artifact = self.Data_validation(data_ingestion_artifact=data_ingestion_artifact)
            logging.info(f"Data Validation completed. Status: {data_validation_artifact.validation_status}")
            logging.info(f"Validation report: {data_validation_artifact.validation_report_file_path}")
            
            # Step 3: Data Transformation
            logging.info("\n" + "="*80)
            logging.info("Step 3: Data Transformation")
            logging.info("="*80)
            data_transformation_artifact = self.Data_Transformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )
            logging.info(f"Data Transformation completed. Transformed train file: {data_transformation_artifact.transformed_trained_file_path}")
            logging.info(f"Transformed test file: {data_transformation_artifact.transformed_test_file_path}")
            
            # Step 4: Model Training
            logging.info("\n" + "="*80)
            logging.info("Step 4: Model Training")
            logging.info("="*80)
            model_training_artifact = self.Model_Training(
                data_transformation_artifact=data_transformation_artifact
            )
            logging.info(f"Model Training completed. Model saved at: {model_training_artifact.trained_model_path}")
            
            # Step 5: Model Evaluation
            logging.info("\n" + "="*80)
            logging.info("Step 5: Model Evaluation")
            logging.info("="*80)
            model_evaluation_artifact = self.Model_Evaluation(
                model_training_artifact=model_training_artifact,
                data_transformation_artifact=data_transformation_artifact
            )
            logging.info(f"Model Evaluation completed. Accuracy: {model_evaluation_artifact.accuracy}")
            logging.info(f"Model Accepted: {model_evaluation_artifact.is_model_accepted}")
            logging.info(f"Evaluation report: {model_evaluation_artifact.model_test_report_file_path}")
            
            # Step 6: Model Pusher
            logging.info("\n" + "="*80)
            logging.info("Step 6: Model Pusher")
            logging.info("="*80)
            model_pusher_artifact = self.Model_Pusher(
                model_evaluation_artifact=model_evaluation_artifact
            )
            logging.info(f"Model Pusher completed. Model pushed: {model_pusher_artifact.is_model_pushed}")
            if model_pusher_artifact.is_model_pushed:
                logging.info(f"Production model path: {model_pusher_artifact.saved_model_path}")
            logging.info(f"Pusher artifact directory: {model_pusher_artifact.model_pusher_dir}")
            
            logging.info("\n" + "="*80)
            logging.info("Training Pipeline Completed Successfully!")
            logging.info("="*80)
            
        except Exception as e:
            logging.error(f"Error in training pipeline: {str(e)}")
            raise MyException(e, sys) from e    
        

        

        