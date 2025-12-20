import pandas as pd
import sys
from src.logger import logging
from src.exception import MyException
import pymongo
import os


class DataLoad:
    """
    This Class iuse to load the data into Dataware house for future ML work
    """
    def __init__(self,df):
        self.df = df

    def load_data_MongoDB(self):
        """
        This method is used to the Load the extract data in our Dataware house that is MongoDB
        """
        try:
            logging.info("Converting the data into the Dictionary....")
            data = self.df.to_dict(orient='records')
            
            # Convert datetime.date and datetime.time objects to strings for MongoDB compatibility
            logging.info("Converting datetime objects to strings for MongoDB compatibility...")
            for record in data:
                for key, value in record.items():
                    # Convert date objects to ISO format string
                    if hasattr(value, 'isoformat'):
                        record[key] = value.isoformat()

            DB_NAME = "Soccer-Data"
            COLLECTION_NAME = "PremierLeague-Matches-Data"
            
            logging.info("Make a connection with the MONGODB...")
            logging.info("Making a database and Collection...")

            CONNECTION_URL = os.getenv("MONGODB_URL")

            client = pymongo.MongoClient(CONNECTION_URL)
            data_base = client[DB_NAME]
            collection = data_base[COLLECTION_NAME]

            logging.info("Push the data into Database")
            rec = collection.insert_many(data)
            logging.info("Successfully inserted {} records into MongoDB".format(len(rec.inserted_ids)))
                    
        except Exception as e:
            logging.error("Error occurred during MongoDB data load: {}".format(str(e)))
            raise MyException(str(e), sys)