import pandas as pd
from src.logger import logging
from src.exception import MyException

import warnings
warnings.filterwarnings('ignore')


class DataTransformation:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def transform_pl_data(self):
        try:
            logging.info("Starting data transformation")
            columns_to_keep = [
                "date", "home_team", "away_team", "FTHG", "FTAG",
                "HS", "AS", "HST", "AST",
                "HF", "AF", "HC", "AC",
                "HY", "AY", "HR", "AR",
                "HTHG", "HTAG"
            ]

            logging.info("Selecting relevant columns")
            df_pl = self.df[columns_to_keep].copy()

            logging.info("Renaming columns")
            df_pl = df_pl.rename(columns={
                "FTHG": "home_goals",
                "FTAG": "away_goals",
                "HS": "home_shots",
                "AS": "away_shots",
                "HST": "home_shots_on_target",
                "AST": "away_shots_on_target",
                "HF": "home_fouls",
                "AF": "away_fouls",
                "HC": "home_corners",
                "AC": "away_corners",
                "HY": "home_yellow",
                "AY": "away_yellow",
                "HR": "home_red",
                "AR": "away_red",
                "HTHG": "home_ht_goals",
                "HTAG": "away_ht_goals"
            })

            logging.info("Extracting time and date components")
            df_pl['time'] = df_pl['date'].dt.time

            df_pl['date'] = df_pl['date'].dt.date

            logging.info("Sorting data by date and time")
            df_pl = df_pl.sort_values(by=['date', 'time'])

            logging.info("Resetting index")
            df_pl.reset_index(drop=True, inplace=True)

            logging.info("Data transformation completed. Total records: {}".format(len(df_pl)))
            return df_pl
        except Exception as e:
            logging.error("Error occurred during data transformation: {}".format(str(e)))
            raise MyException(e)
