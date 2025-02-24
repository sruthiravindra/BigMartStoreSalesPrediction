from salesPrediction.config.configuration import ConfigurationManager
from salesPrediction.components.data_transformation import DataTransformation
from salesPrediction import logger
from pathlib import Path

STAGE_NAME = "Data Transformation"


class DataTransformationPipeLine:
    def __init__(self, validation_status:bool):
        self.validation_status = validation_status

    def main(self):
        try:
            
            if self.validation_status == True:
                config = ConfigurationManager()
                data_transformation_config = config.get_data_transformation_config()
                data_transformation = DataTransformation(config=data_transformation_config)
                data_transformation.train_test_splitting()
            else:
                raise Exception("Your dataset is not valid")
        except Exception as e:
            logger.info(e)
            raise Exception(e)
        
if __name__ == "__main__":
    try:
        logger.info(f">>>> stage {STAGE_NAME} started <<<<")
        obj = DataTransformationPipeLine(True)
        obj.main()
        logger.info(f">>>> stage {STAGE_NAME} completed <<<<")

    except Exception as e:
        logger.exception(e)
        raise(e)