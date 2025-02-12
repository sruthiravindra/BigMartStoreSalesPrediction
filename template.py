import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "BigMartStoreSalesPrediction"

list_of_files = [
    f"src/salesPrediction/__init__.py",
    f"src/salesPrediction/components/__init__.py",
    f"src/salesPrediction/utils/__init__.py",
    f"src/salesPrediction/utils/common.py",
    f"src/salesPrediction/config/__init__.py",
    f"src/salesPrediction/config/configuration.py",
    f"src/salesPrediction/pipeline/__init__.py",
    f"src/salesPrediction/entity/__init__.py",
    f"src/salesPrediction/entity/config_entity.py",
    f"src/salesPrediction/constants/__init__.py",
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
    "main.py",
    "app.py",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb",
    "templates/index.html"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    print(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")
    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists.")