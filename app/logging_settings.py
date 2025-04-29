import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_format = "%(asctime)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)

file_handler = RotatingFileHandler(
    "jobs_telegram.log",
    maxBytes=4_000,
    backupCount=1
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
