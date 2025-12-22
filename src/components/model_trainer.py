import pandas as pd
import sys
import os
import pickle

from src.exception import MyException
from src.logger import logging
from src.entity.artifact_entity import DataTransformationArtifcat, ModelTrainingArtifact
from src.entity.config_entity import ModelTrainingConfig


class ModelTraining:
    def __init__(self, data_transformation_artifact : DataTransformationArtifcat, model_training_config:ModelTrainingConfig):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_training_config = model_training_config
        except Exception as e:
            raise MyException(e,sys)
    
    def initiate_model_training(self) -> ModelTrainingArtifact:
        """
        Model Training Component: Trains the machine learning model on transformed training data
        This component ONLY handles model training. Model evaluation is done in a separate component.
        """
        try:
            logging.info("Entered the model_training method")
            
            # Load the train transformed data
            logging.info(f"Loading training data from: {self.data_transformation_artifact.transformed_trained_file_path}")
            train_df = pd.read_csv(self.data_transformation_artifact.transformed_trained_file_path)
            logging.info(f"Training data shape: {train_df.shape}")

            input_features = ['hour',
                    'home_shots_on_target_avg_last5',
                    'away_shots_on_target_avg_last5',
                    'home_shots_avg_last5',
                    'away_shots_avg_last5',
                    'home_team_goals_conceded_avg_last5',
                    'away_team_goals_conceded_avg_last5',
                    'home_goals_avg_last5',
                    'away_goals_avg_last5',
                    'home_points_last5_matches',
                    'away_points_last5_matches',
                    'points_diff_last5',
                    'goal_diff_avg5',
                    'shots_diff_avg5',
                    'x_defense_diff',
                    'home_advantage',
                    'shots_on_target_diff_avg5']
            
            logging.info(f"Selected {len(input_features)} input features")
            X_train = train_df[input_features]
            y_train = train_df['result']
            
            logging.info(f"Features shape: {X_train.shape}, Target shape: {y_train.shape}")

            # Initialize and train the model
            logging.info("Initializing AdaBoost model")
            model = self.model_training_config.model
            
            logging.info("Training model started...")
            model.fit(X_train, y_train)
            logging.info("Model training completed successfully")
            
            # Create model directory if it doesn't exist
            os.makedirs(self.model_training_config.model_training_dir, exist_ok=True)
            
            # Save the trained model
            model_path = os.path.join(self.model_training_config.model_training_dir_name)
            logging.info(f"Saving trained model to: {model_path}")
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
            logging.info("Model saved successfully")
            
            # Create and return ModelTrainingArtifact
            model_training_artifact = ModelTrainingArtifact(
                trained_model_path=model_path
            )
            
            logging.info("Exited the model_training method")
            return model_training_artifact
            
        except Exception as e:
            logging.error(f"Error in model training: {str(e)}")
            raise MyException(e, sys)

