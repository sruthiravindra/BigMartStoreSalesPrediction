from salesPrediction import logger
from salesPrediction.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from salesPrediction.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from salesPrediction.pipeline.stage_03_data_transformation import DataTransformationPipeLine

STAGE_NAME="Data Ingestion Stage"
try:
    logger.info(f">>>> stage {STAGE_NAME} started <<<<")
    obj = DataIngestionTrainingPipeline()
    obj.main()
    logger.info(f">>>> stage {STAGE_NAME} completed <<<<")
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME="Data Validation Stage"
try:
    logger.info(f">>>> stage {STAGE_NAME} started <<<<")
    obj = DataValidationTrainingPipeline()
    status = obj.main()
    logger.info(f">>>> stage {STAGE_NAME} completed with status {status}<<<<")
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME="Data Transformation Stage"
try:
    logger.info(f">>>> stage {STAGE_NAME} started {status} <<<<")
    obj = DataTransformationPipeLine(status)
    obj.main()
    logger.info(f">>>> stage {STAGE_NAME} completed <<<<")
except Exception as e:
    logger.exception(e)
    raise e