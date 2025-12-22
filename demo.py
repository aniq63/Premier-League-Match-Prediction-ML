# # from ETL.etl_piepline import ETLPipeline

# # pipeline = ETLPipeline(seasons=[2021, 2022, 2023, 2024, 2025])
# # result = pipeline.run()

# from src.pipline.training_pipeline import Training_Piepline

# pipeline = Training_Piepline()
# result = pipeline.run_pipeline()


"""
Test script to run the complete training pipeline
"""
from src.pipline.training_pipeline import Training_Piepline
from src.logger import logging

if __name__ == "__main__":
    try:
        logging.info("Initializing Training Pipeline Test")
        pipeline = Training_Piepline()
        pipeline.run_pipeline()
        logging.info("Pipeline test completed successfully!")
    except Exception as e:
        logging.error(f"Pipeline test failed: {str(e)}")
        raise e
