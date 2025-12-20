# from ETL.etl_piepline import ETLPipeline

# pipeline = ETLPipeline(seasons=[2021, 2022, 2023, 2024, 2025])
# result = pipeline.run()

from src.pipline.training_pipeline import Training_Piepline

pipeline = Training_Piepline()
result = pipeline.run_pipeline()