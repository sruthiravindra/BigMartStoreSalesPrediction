from salesPrediction.config.configuration import ConfigurationManager
from salesPrediction.components.data_validation import DataValidation
from salesPrediction import logger
from typing import Tuple, Dict, Any

STAGE_NAME = "Data Validation"

class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self) -> Tuple[bool, Dict[str, Any]]:
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(data_validation_config)
        data_validation.validate_all_columns()
        mismatched_cols = data_validation.validate_column_datatype()
        status = bool(data_validation.get_validation_status())
        return status, mismatched_cols

if __name__ == "__main__":
    try:
        logger.info(f">>>> stage {STAGE_NAME} started <<<<")
        obj = DataValidationTrainingPipeline()
        status, mismatched_cols = obj.main()
        logger.info(f">>>> stage {STAGE_NAME} completed with status {status}<<<<")

    except Exception as e:
        logger.exception(e)
        raise(e)