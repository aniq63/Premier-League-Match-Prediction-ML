from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path : str
    test_file_path : str

@dataclass
class DataValidationArtifact:
    validation_status:bool
    message: str
    validation_report_file_path: str

@dataclass
class DataTransformationArtifcat:
    transformed_trained_file_path : str
    transformed_test_file_path : str

@dataclass
class ModelTrainingArtifact:
    trained_model_path : str

@dataclass
class ModelEvaluationArtifact:
    accuracy : float
    model_test_report_file_path : str
    is_model_accepted: bool
    model_path: str

@dataclass
class ModelPusherArtifact:
    model_pusher_dir: str
    saved_model_path: str
    is_model_pushed: bool