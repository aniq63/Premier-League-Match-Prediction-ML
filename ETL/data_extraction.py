import soccerdata as sd
import pandas as pd
from src.logger import logging
from src.exception import MyException
import sys
import warnings
warnings.filterwarnings('ignore')


class DataExtraction:
    def __init__(self, seasons:list):
        self.seasons = seasons

    def extract_pl_data(self):
        """
        This method is used to extrct pl data using the seasons parameter
        """
        try:
            logging.info("Starting data extraction for seasons: {}".format(self.seasons))
            all_games_df = []
            for x in self.seasons:
                logging.info("Extracting data for season: {}".format(x))
                mh = sd.MatchHistory(leagues="ENG-Premier League", seasons=x)
                games_df = mh.read_games()
                all_games_df.append(games_df)
                logging.info("Successfully extracted data for season: {}".format(x))

            df = pd.concat(all_games_df)
            logging.info("Data extraction completed. Total records: {}".format(len(df)))
            return df
        except Exception as e:
            logging.error("Error occurred during data extraction: {}".format(str(e)))
            raise MyException(e,sys)      
        
