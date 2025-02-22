import os
from salesPrediction import logger
import pandas as pd
from salesPrediction.config.configuration import DataValidationConfig

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

    def validate_datatype(self) -> bool:
        try:
            validation_status = None

            data = pd.read_csv(self.config.unzip_data_dir)
            all_cols = list(data.columns)
            col_types = data.dtypes.to_dict()

            all_schema = self.config.all_schema

            for col in all_cols:
                if col not in all_schema:
                    validation_status = False
                    with open(self.config.STATUS_FILE, "w") as f:
                        f.write(f"Validation Status col not found {col}: {validation_status}")
                else:
                    if data[col].dtype != all_schema[col]:
                        validation_status = False
                        with open(self.config.STATUS_FILE, "w") as f:
                            f.write(f"Validation Status col type mismatch {col}: {validation_status}")
                    else:
                        validation_status = True
                        with open(self.config.STATUS_FILE, "w") as f:
                            f.write(f"Validation Status col {col}: {validation_status}")
        except Exception as e:
            raise e

        