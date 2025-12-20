import pandas as pd
import sys
from src.logger import logging
from src.exception import MyException
from ETL.data_extraction import DataExtraction
from ETL.data_transformation import DataTransformation
from ETL.data_load import DataLoad
import warnings

warnings.filterwarnings('ignore')


class ETLPipeline:
    """
    This class orchestrates the entire ETL (Extract, Transform, Load) pipeline
    for Premier League match data processing.
    """

    def __init__(self, seasons: list):
        """
        Initialize the ETL Pipeline with seasons

        Args:
            seasons (list): List of seasons to extract data for
        """
        try:
            logging.info("Initializing ETL Pipeline with seasons: {}".format(seasons))
            self.seasons = seasons
            self.extracted_df = None
            self.transformed_df = None
        except Exception as e:
            logging.error("Error occurred during ETL Pipeline initialization: {}".format(str(e)))
            raise MyException(str(e), sys)

    def extract_data(self):
        """
        Execute the data extraction step

        Returns:
            pd.DataFrame: Extracted data from Premier League
        """
        try:
            logging.info("Starting data extraction step...")
            data_extraction = DataExtraction(seasons=self.seasons)
            self.extracted_df = data_extraction.extract_pl_data()
            logging.info("Data extraction step completed successfully")
            return self.extracted_df
        except Exception as e:
            logging.error("Error occurred during data extraction step: {}".format(str(e)))
            raise MyException(str(e), sys)

    def transform_data(self):
        """
        Execute the data transformation step

        Returns:
            pd.DataFrame: Transformed data
        """
        try:
            if self.extracted_df is None:
                logging.warning("Extracted data is None. Running extraction first...")
                self.extract_data()

            logging.info("Starting data transformation step...")
            data_transformation = DataTransformation(df=self.extracted_df)
            self.transformed_df = data_transformation.transform_pl_data()
            logging.info("Data transformation step completed successfully")
            return self.transformed_df
        except Exception as e:
            logging.error("Error occurred during data transformation step: {}".format(str(e)))
            raise MyException(str(e), sys)

    def load_data(self):
        """
        Execute the data load step

        Returns:
            bool: True if loading was successful
        """
        try:
            if self.transformed_df is None:
                logging.warning("Transformed data is None. Running transformation first...")
                self.transform_data()

            logging.info("Starting data load step...")
            data_load = DataLoad(df=self.transformed_df)
            data_load.load_data_MongoDB()
            logging.info("Data load step completed successfully")
            return True
        except Exception as e:
            logging.error("Error occurred during data load step: {}".format(str(e)))
            raise MyException(str(e), sys)

    def run(self):
        """
        Execute the complete ETL pipeline (Extract -> Transform -> Load)

        Returns:
            dict: Pipeline execution status and results
        """
        try:
            logging.info("=" * 60)
            logging.info("Starting ETL Pipeline execution...")
            logging.info("=" * 60)

            # Step 1: Extract
            logging.info("STEP 1: Data Extraction")
            logging.info("-" * 60)
            self.extract_data()

            # Step 2: Transform
            logging.info("STEP 2: Data Transformation")
            logging.info("-" * 60)
            self.transform_data()

            # Step 3: Load
            logging.info("STEP 3: Data Load")
            logging.info("-" * 60)
            self.load_data()

            logging.info("=" * 60)
            logging.info("ETL Pipeline execution completed successfully!")
            logging.info("=" * 60)

            return {
                "status": "SUCCESS",
                "extracted_records": len(self.extracted_df),
                "transformed_records": len(self.transformed_df),
                "message": "ETL Pipeline completed successfully"
            }

        except Exception as e:
            logging.error("=" * 60)
            logging.error("ETL Pipeline execution failed!")
            logging.error("Error: {}".format(str(e)))
            logging.error("=" * 60)
            raise MyException(str(e), sys)

    def get_extracted_data(self):
        """
        Get the extracted data

        Returns:
            pd.DataFrame: Extracted data
        """
        return self.extracted_df

    def get_transformed_data(self):
        """
        Get the transformed data

        Returns:
            pd.DataFrame: Transformed data
        """
        return self.transformed_df
