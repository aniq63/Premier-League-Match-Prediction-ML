import os
import sys

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.data_access.EPL_data import EplData

from src.logger import logging
from src.exception import MyException

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            logging.info("Initializing DataIngestion class")
            self.data_ingestion_config = data_ingestion_config
            logging.info("DataIngestion class initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing DataIngestion: {str(e)}")
            raise MyException(e, sys)

    def export_data_as_dataframe(self):
        try:
            logging.info(f"Exporting data from collection: {self.data_ingestion_config.collection_name}")
            data = EplData()
            df = data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            logging.info(f"Successfully exported data with shape: {df.shape}")
            return df
            
        except Exception as e:
            logging.error(f"Error while exporting data: {str(e)}")
            raise MyException(e, sys)
        
    def split_data(self,df):
        try:
            split_date = self.data_ingestion_config.split_date
            logging.info(f"Splitting data with split date: {split_date}")
            
            train_data = df[df['date'] < split_date]
            test_data = df[df['date'] >= split_date]
            
            logging.info(f"Training data shape: {train_data.shape}, Test data shape: {test_data.shape}")
            return train_data,test_data
        except Exception as e:
            logging.error(f"Error while splitting data: {str(e)}")
            raise MyException(e, sys)
    
    def initiate_DataIngestion(self):
        try:
            logging.info("Starting data ingestion process")
            df = self.export_data_as_dataframe()

            ingestion_file_path = os.path.dirname(self.data_ingestion_config.raw_file_path)
            os.makedirs(ingestion_file_path, exist_ok=True)
            logging.info(f"Created directory: {ingestion_file_path}")

            df.to_csv(self.data_ingestion_config.raw_file_path, index=False, header=True)
            logging.info(f"Raw data saved to: {self.data_ingestion_config.raw_file_path}")

            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.raw_file_path,
            test_file_path=self.data_ingestion_config.raw_file_path)
            
            logging.info("Data ingestion completed successfully")
            return data_ingestion_artifact
        except Exception as e:
            logging.error(f"Error during data ingestion: {str(e)}")
            raise MyException(e, sys)


