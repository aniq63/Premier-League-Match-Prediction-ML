import pickle
import pandas as pd
import os
import yaml
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from src.exception import MyException
from src.logger import logging
from src.entity.artifact_entity import ModelTrainingArtifact, ModelEvaluationArtifact,DataTransformationArtifcat
from src.entity.config_entity import ModelEvaluationConfig
import sys

class ModelEvaluation:
    def __init__(self, model_training_artifact: ModelTrainingArtifact, 
                 data_transformation_artifact:DataTransformationArtifcat, 
                 model_evaluation_config: ModelEvaluationConfig):
        
        self.model_training_artifact = model_training_artifact
        self.data_transformation_artifact = data_transformation_artifact
        self.model_evaluation_config = model_evaluation_config

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        """
        Model Evaluation Component: Evaluates trained model on test data and generates report
        """
        try:
            logging.info("Entered the model_evaluation method")
            
            # Create model evaluation directory
            os.makedirs(self.model_evaluation_config.model_evaluation_dir, exist_ok=True)
            logging.info(f"Model evaluation directory created: {self.model_evaluation_config.model_evaluation_dir}")
            
            # Load trained model
            logging.info(f"Loading trained model from: {self.model_training_artifact.trained_model_path}")
            with open(self.model_training_artifact.trained_model_path, 'rb') as f:
                model = pickle.load(f)
            logging.info("Model loaded successfully")
            
            # Load test data
            logging.info(f"Loading test data from: {self.data_transformation_artifact.transformed_test_file_path}")
            test_df = pd.read_csv(self.data_transformation_artifact.transformed_test_file_path)
            logging.info(f"Test data shape: {test_df.shape}")
            
            # Features (same as training)
            input_features = [
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
            
            logging.info(f"Extracting features: {len(input_features)} features")
            X_test = test_df[input_features]
            y_test = test_df['result']
            logging.info(f"Features shape: {X_test.shape}, Target shape: {y_test.shape}")
            
            # Make predictions
            logging.info("Making predictions on test data...")
            y_pred = model.predict(X_test)
            logging.info("Predictions completed")
            
            # Calculate metrics
            logging.info("Calculating evaluation metrics...")
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            f1 = f1_score(y_test, y_pred, average='weighted')

            model_path = self.model_training_artifact.trained_model_path
            
            logging.info(f"Model Evaluation Metrics - Accuracy: {accuracy:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}, F1: {f1:.4f}")
            
            # Create evaluation report
            evaluation_report = {
                'accuracy': float(accuracy),
                'precision': float(precision),
                'recall': float(recall),
                'f1_score': float(f1),
                'expected_accuracy': self.model_evaluation_config.expected_accuracy,
                'model_path': model_path
            }
            
            # Save report to YAML file
            report_file_path = self.model_evaluation_config.model_evaluation_dir_name
            os.makedirs(os.path.dirname(report_file_path), exist_ok=True)
            
            logging.info(f"Saving evaluation report to: {report_file_path}")
            with open(report_file_path, 'w') as f:
                yaml.dump(evaluation_report, f)
            logging.info("Evaluation report saved successfully")
            
            # Check if meets threshold
            is_model_accepted = accuracy >= self.model_evaluation_config.expected_accuracy
            
            if is_model_accepted:
                logging.info(f"Model ACCEPTED! Accuracy {accuracy:.4f} >= Threshold {self.model_evaluation_config.expected_accuracy}")
            else:
                logging.warning(f"Model REJECTED! Accuracy {accuracy:.4f} < Threshold {self.model_evaluation_config.expected_accuracy}")
            
            # Create artifact
            model_evaluation_artifact = ModelEvaluationArtifact(
                accuracy=round(accuracy, 4),
                model_test_report_file_path=report_file_path,
                is_model_accepted=is_model_accepted,
                model_path=model_path
            )
            
            logging.info("Exited the model_evaluation method")
            return model_evaluation_artifact
            
        except Exception as e:
            logging.error(f"Error in model evaluation: {str(e)}")
            raise MyException(e, sys)