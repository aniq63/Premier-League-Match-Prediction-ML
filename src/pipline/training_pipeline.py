from src.entity.config_entity import DataIngestionConfig, DataValidationConfig
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.exception import MyException
from src.logger import logging
import sys


class Training_Piepline:
    def __init__(self):
        logging.info("Initializing Training Pipeline")
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()

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
        


    def Data_validation(self,data_ingestion_artifact) -> DataValidationArtifact:
        try:
            logging.info("Entered the data_validation method of TrainPipeline class")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=self.data_validation_config)
            data_validation_artifcat = data_validation.initiate_data_validation()
            logging.info("Exited the data_validation method of TrainPipeline class")
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e,sys) from e

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.Data_Ingestion()
            data_validation_artifact = self.Data_validation(data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise MyException(e,sys) from e    
        

        

        