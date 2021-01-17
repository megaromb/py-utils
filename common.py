import logging
import coloredlogs
from pathlib import Path


def init_logger(logger_name: str):
    logger = logging.getLogger(logger_name)
    coloredlogs.install(level="DEBUG", milliseconds=True)
    return logger


def get_file_name_without_ext(file_path: str):
    return Path(__file__).stem
