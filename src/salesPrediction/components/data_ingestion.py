import os
import urllib.request as request
import zipfile
from salesPrediction import logger
from salesPrediction.utils.common import get_size
from salesPrediction.entity.config_entity import DataIngestionConfig
from pathlib import Path


class DataIngestion:
    def __init__(self, config:DataIngestionConfig):
        self.config = config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, header = request.urlretrieve(
                url = self.config.source_URL,
                filename= self.config.local_data_file
            )
            logger.info(f"{filename} downloaded with following info: \n{header}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")
    
    def extract_zip_file(self):
        """
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, "r") as zip_ref:
            zip_ref.extractall(unzip_path)

