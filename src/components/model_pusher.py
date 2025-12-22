import shutil
import os
from src.exception import MyException
from src.logger import logging
from src.entity.artifact_entity import ModelEvaluationArtifact, ModelPusherArtifact
from src.entity.config_entity import ModelPusherConfig
import sys

class ModelPusher:
    def __init__(self, model_evaluation_artifact: ModelEvaluationArtifact, 
                 model_pusher_config: ModelPusherConfig):
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        Model Pusher Component: Pushes accepted model to production directory
        Returns ModelPusherArtifact with push status and paths
        """
        try:
            logging.info("Entered the model_pusher method")
            
            # Create model pusher directory in artifacts
            os.makedirs(self.model_pusher_config.model_pusher_dir, exist_ok=True)
            logging.info(f"Created model pusher directory: {self.model_pusher_config.model_pusher_dir}")
            
            is_model_pushed = False
            saved_model_path = None
            
            if self.model_evaluation_artifact.is_model_accepted:
                logging.info(f"Model ACCEPTED - Accuracy: {self.model_evaluation_artifact.accuracy}")
                logging.info(f"Model accepted. Pushing to production...")
                
                # Create saved models directory if it doesn't exist
                os.makedirs(self.model_pusher_config.saved_model_dir, exist_ok=True)
                logging.info(f"Created saved models directory: {self.model_pusher_config.saved_model_dir}")
                
                # Copy model to artifact directory
                artifact_model_path = os.path.join(self.model_pusher_config.model_pusher_dir, "model.pkl")
                logging.info(f"Copying model to artifact directory: {artifact_model_path}")
                shutil.copy(
                    self.model_evaluation_artifact.model_path,
                    artifact_model_path
                )
                
                # Copy model to production directory
                logging.info(f"Copying model from: {self.model_evaluation_artifact.model_path}")
                logging.info(f"Pushing model to production: {self.model_pusher_config.saved_model_path}")
                
                shutil.copy(
                    self.model_evaluation_artifact.model_path,
                    self.model_pusher_config.saved_model_path
                )
                
                saved_model_path = self.model_pusher_config.saved_model_path
                is_model_pushed = True
                logging.info(f"Model successfully pushed to production: {saved_model_path}")
            else:
                logging.warning(f"Model REJECTED - Accuracy: {self.model_evaluation_artifact.accuracy} is below threshold")
                logging.info("Model rejected. Not pushing to production.")
            
            # Create and return artifact
            model_pusher_artifact = ModelPusherArtifact(
                model_pusher_dir=self.model_pusher_config.model_pusher_dir,
                saved_model_path=saved_model_path if is_model_pushed else "Model not pushed",
                is_model_pushed=is_model_pushed
            )
            
            logging.info("Exited the model_pusher method")
            return model_pusher_artifact
            
        except Exception as e:
            logging.error(f"Error in model pusher: {str(e)}")
            raise MyException(e, sys)