import os
from salesPrediction import logger
from sklearn.model_selection import train_test_split
import pandas as pd
from salesPrediction.config.configuration import DataTransformationConfig
import json

class DataTransformation:
    def __init__(self, config:DataTransformationConfig):
        self.config = config
    
    def train_test_splitting(self):
        # we already have train and test data set in the resources folder, we only need to copy them 
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)
        
        train_data.to_csv(os.path.join(self.config.data_path, "Train.csv"), index=False)
        test_data.to_csv(os.path.join(self.config.data_path, "Test.csv"), index= False)

        logger.info("Completed saving train and test data to transformation folder")
        logger.info(train_data.shape)
        logger.info(test_data.shape)

        print(train_data.shape)
        print(test_data.shape)
    
    def convert_column_datatype(self):
        try:

            with open(self.config.mismatch_data_type_path, "r") as f:
                mismatched_cols =  json.loads(f.read())

            data = pd.read_csv(self.config.train_data_path)
            for col, dtype_info in mismatched_cols.items():
                if dtype_info == "string":
                    data[col].astype("string")
                    logger.info("Converted data type of column {col} to {dtype_info}")


        except Exception as e:
            raise e