import os
from salesPrediction import logger
import pandas as pd
from salesPrediction.config.configuration import DataValidationConfig
import json

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self)-> bool:
        try:
            validation_status = None

            data = pd.read_csv(self.config.unzip_data_dir)
            all_cols = list(data.columns)

            all_schema = self.config.all_schema.keys()

            for col in all_cols:
                if col not in all_schema:
                    validation_status = False
                    with open(self.config.STATUS_FILE, "w") as f:
                        f.write(f"Validation Status col {col}: {validation_status}")
                else:
                    validation_status = True
                    with open(self.config.STATUS_FILE, "w") as f:
                        f.write(f"Validation Status col {col}: {validation_status}")

            return validation_status
        except Exception as e:
            raise e

    def validate_column_datatype(self) -> dict:
        try:
            validation_status = None

            data = pd.read_csv(self.config.unzip_data_dir)

            all_schema = self.config.all_schema
            mismatched_cols = {}
            
            for col in all_schema:
                if data[col].dtype != all_schema[col]:
                    
                    validation_status = "DATATYPE_MISMATCH"

                    actual_type = str(data[col].dtype)
                    expected_type = all_schema[col]

                    mismatched_cols[col] = {"expected" : expected_type, "actual" : actual_type}
                    
            if validation_status == "DATATYPE_MISMATCH":
                with open(self.config.STATUS_FILE, "w") as f:
                        f.write(f"Validation Status : {validation_status}")

                with open(self.config.STATUS_DATA_TYPE_FILE, "w") as f:
                        json.dump(mismatched_cols, f, indent=4)

            return mismatched_cols
        except Exception as e:
            raise e
        
    def get_validation_status(self) -> bool:

        with open(self.config.STATUS_FILE, "r") as f:
            status = f.read().split(" ")[-1]

        return status


        