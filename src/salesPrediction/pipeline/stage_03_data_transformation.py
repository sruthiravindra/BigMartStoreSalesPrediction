from salesPrediction.config.configuration import ConfigurationManager
from salesPrediction.components.data_transformation import DataTransformation
from salesPrediction.utils.common import get_validation_status
from salesPrediction import logger
from pathlib import Path
from typing import Dict

STAGE_NAME = "Data Transformation"


class DataTransformationPipeLine:
    def __init__(self):
        pass

    def main(self):
        try:

            # check if data type mismatch present
            validation_status = get_validation_status()
            logger.info(f" validation status ::  {validation_status}")

            if validation_status != False:

                config = ConfigurationManager()
                data_transformation_config = config.get_data_transformation_config()
                data_transformation = DataTransformation(config=data_transformation_config)

                # check if any datatype mismatch has occurred
                if validation_status == "DATATYPE_MISMATCH":
                    data_transformation.convert_column_datatype()            
                
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