import logging
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)

log_filename = datetime.now().strftime("logs/%Y-%m-%d_%H-%M-%S.log")

logger = logging.getLogger("GraphRAG-CellTypeAnnotation")
logger.setLevel(logging.INFO)

if not logger.handlers:

    file_handler = logging.FileHandler(log_filename)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
