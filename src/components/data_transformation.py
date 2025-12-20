import pandas as pd
import numpy as np
import sys
import os

from pandas import DataFrame

from src.exception import MyException
from src.logger import logging
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifcat
from src.entity.config_entity import DataTransformationConfig


class DataTransformation:
    def __init__(
            self,
            data_ingestion_artifact : DataIngestionArtifact,
            data_validtaion_artifact : DataValidationArtifact,
            data_transformation_config : DataTransformationConfig
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validtaion_artifact = data_validtaion_artifact
            self.data_transformation_config = data_transformation_config
            logging.info("DataTransformation class initialized successfully")
        except Exception as e:
            logging.error(f"Error during DataTransformation initialization: {str(e)}")
            raise MyException(e, sys)
        
    def feature_engineering(self, df) -> pd.DataFrame:
        try:
            logging.info("Starting feature engineering")            

            # Create match result column
            df["result"] = df.apply(
                           lambda row: "Win" if row["home_goals"] > row["away_goals"]
                           else "Draw" if row["home_goals"] == row["away_goals"]
                           else "Lose",
                            axis=1
                        )
            
            # Convert the String type columns to DateTime
            df['date'] = pd.to_datetime(df['date'])
            df['time'] = pd.to_datetime(df['time'])

            # Extract the starting hour from date column if not already present
            if "hour" not in df.columns or df["hour"].isnull().any():
                df["hour"] = df["time"].dt.hour
            
            # Add new column of goals conceded by home and away team
            df["away_team_goals_conceded"] = df['home_goals']
            df['home_team_goals_conceded']  = df["away_goals"]

            df = df[[
                 # Just for information purpose not need in training
                 "date",
                 "home_team",
                 "away_team",
                 # Columsn for training purposes
                 "hour",
                 "home_goals",
                 "away_goals",
                 "home_shots_on_target",
                 "away_shots_on_target",
                 'home_team_goals_conceded',
                 'away_team_goals_conceded',
                 'home_shots',
                 'away_shots',
                 # Target Column
                 'result'
            ]]

            logging.info("Feature engineering completed successfully")
            return df

        except Exception as e:
            logging.error(f"Error during feature engineering: {str(e)}")
            raise MyException(e, sys)
        

    # Redefine the rolling_averages function with corrections
    def rolling_averages(self, group, cols, new_cols):
        try:
            logging.info(f"Calculating rolling averages for columns: {cols}")
            
            group = group.sort_values("date")
            rolling_stats = group[cols].rolling(5, closed='left').mean()
            group[new_cols] = rolling_stats
            group = group.dropna(subset=new_cols)
            
            logging.info("Rolling averages calculated successfully")
            return group
        except Exception as e:
            logging.error(f"Error during rolling averages calculation: {str(e)}")
            raise MyException(e, sys)
            

    def add_points_rolling_columns(self, df):
        try:
            logging.info("Adding points rolling columns")
            
            home = df[["date", "home_team", "home_goals", "away_goals"]].rename(
                columns={"home_team": "team",
                         "home_goals": "goals_scored",
                         "away_goals": "goals_conceded"
                         }
            )

            away = df[["date", "away_team", "home_goals", "away_goals"]].rename(
                columns={"away_team": "team",
                         "home_goals": "goals_conceded",
                         "away_goals": "goals_scored"
                }
            )

            team_matches = pd.concat([home, away], ignore_index=True)
            team_matches.sort_values(["date", "team"], inplace=True)

            team_matches['point'] = np.where(
                team_matches['goals_scored'] > team_matches['goals_conceded'], 3,
                np.where(team_matches['goals_scored'] == team_matches['goals_conceded'], 1, 0)
            )

            team_matches["points_last5_matches"] = (
                team_matches.groupby("team")["point"].rolling(5).sum().reset_index(0, drop=True)
            )

            team_matches.dropna(subset=['points_last5_matches'], inplace=True)

            df = df.merge(
                team_matches[["date", "team", "points_last5_matches"]],
                left_on=["date", "home_team"],
                right_on=["date", "team"],
                how="left"
            ).rename(columns={
                "points_last5_matches": "home_points_last5_matches"
            }).drop(columns="team")

            df = df.merge(
                team_matches[["date", "team", "points_last5_matches"]],
                left_on=["date", "away_team"],
                right_on=["date", "team"],
                how="left"
            ).rename(columns={
                "points_last5_matches": "away_points_last5_matches"
            }).drop(columns="team")

            df.dropna(subset=["home_points_last5_matches", "away_points_last5_matches"], inplace=True)
            
            logging.info("Points rolling columns added successfully")
            return df

        except Exception as e:
            logging.error(f"Error during adding points rolling columns: {str(e)}")
            raise MyException(e, sys)
    
    def add_new_Columns(self, df_final) -> pd.DataFrame:
        try:
            logging.info("Adding new feature columns")
            
            # Add new cols
            df_final["points_diff_last5"] = (df_final["home_points_last5_matches"] - df_final["away_points_last5_matches"])
            df_final["goal_diff_avg5"] = (df_final["home_goals_avg_last5"] - df_final["away_goals_avg_last5"])
            df_final["shots_diff_avg5"] = (df_final["home_shots_avg_last5"] - df_final["away_shots_avg_last5"])
            df_final["shots_on_target_diff_avg5"] = (df_final["home_shots_on_target_avg_last5"] - df_final["away_shots_on_target_avg_last5"])
            df_final["x_defense_diff"] = (df_final["away_team_goals_conceded_avg_last5"] - df_final["home_team_goals_conceded_avg_last5"])
            df_final["home_advantage"] = 1
            
            logging.info("New feature columns added successfully")
            return df_final
        
        except Exception as e:
            logging.error(f"Error during adding new columns: {str(e)}")
            raise MyException(e, sys)
    

    def initiate_data_transformation(self):
        try:
            logging.info("Initiating data transformation")
            
            if self.data_validtaion_artifact.validation_status == True:
                logging.info(f"Validation status is True, loading raw data file")
                # Load the raw data (no split yet)
                df = pd.read_csv(self.data_ingestion_artifact.trained_file_path)
                logging.info(f"Raw data shape: {df.shape}")
            else:
                logging.error("Validation status is False, cannot proceed with data transformation")
                raise ValueError("Data validation failed")
            
            # Feature Engineering
            logging.info("Applying feature engineering")
            df = self.feature_engineering(df)

            # Define columns for rolling averages
            cols = [
                "home_shots_on_target",
                "away_shots_on_target",
                "home_shots",
                "away_shots",
                "home_team_goals_conceded",
                "away_team_goals_conceded",
                "home_goals",
                "away_goals"
            ]

            new_cols = [f"{c}_avg_last5" for c in cols]

            # Apply rolling averages
            logging.info("Calculating rolling averages")
            df = df.groupby("home_team", group_keys=False).apply(lambda x: self.rolling_averages(x, cols, new_cols))

            # Add points rolling columns
            logging.info("Adding points rolling columns")
            df = self.add_points_rolling_columns(df)

            # Drop the Extra columns
            logging.info("Dropping original columns")
            df = df.drop(columns=cols)
            
            # Add new columns
            logging.info("Adding derived feature columns")
            df = self.add_new_Columns(df)

            # Sort and reset index
            logging.info("Sorting and resetting indices")
            df.sort_values('date', inplace=True)
            df.reset_index(inplace=True, drop=True)

            # SPLIT DATA INTO TRAIN AND TEST AFTER ALL TRANSFORMATIONS
            logging.info("Splitting data into train and test sets")
            split_date = self.data_transformation_config.split_date
            logging.info(f"Using split date: {split_date}")
            
            train_df = df[df['date'] < split_date].copy()
            test_df = df[df['date'] >= split_date].copy()
            
            logging.info(f"Training data shape after transformation: {train_df.shape}")
            logging.info(f"Test data shape after transformation: {test_df.shape}")

            # Save transformed data
            logging.info("Creating output directory and saving transformed data")
            transformed_training_file_path = os.path.dirname(self.data_transformation_config.transformed_training_file_path)
            os.makedirs(transformed_training_file_path, exist_ok=True)
            
            train_df.to_csv(self.data_transformation_config.transformed_training_file_path, index=False)
            test_df.to_csv(self.data_transformation_config.transformed_test_file_path, index=False)
            
            logging.info(f"Transformed training data saved to: {self.data_transformation_config.transformed_training_file_path}")
            logging.info(f"Transformed test data saved to: {self.data_transformation_config.transformed_test_file_path}")
            
            # Create and return DataTransformation artifact
            logging.info("Creating DataTransformation artifact")
            data_transformation_artifact = DataTransformationArtifcat(
                transformed_trained_file_path=self.data_transformation_config.transformed_training_file_path,
                transforme_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            
            logging.info("Data transformation completed successfully")
            return data_transformation_artifact
            
        except Exception as e:
            logging.error(f"Error during data transformation: {str(e)}")
            raise MyException(e, sys)

 
              




