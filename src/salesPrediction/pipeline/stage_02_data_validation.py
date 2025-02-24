from salesPrediction.config.configuration import ConfigurationManager
from salesPrediction.components.data_validation import DataValidation
from salesPrediction import logger

STAGE_NAME = "Data Validation"

class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self) -> bool:
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(data_validation_config)
        data_validation.validate_all_columns()
        status = bool(data_validation.get_validation_status())
        return status

if __name__ == "__main__":
    try:
        logger.info(f">>>> stage {STAGE_NAME} started <<<<")
        obj = DataValidationTrainingPipeline()
        status = obj.main()
        logger.info(f">>>> stage {STAGE_NAME} completed with status {status}<<<<")

    except Exception as e:
        logger.exception(e)
        raise(e)