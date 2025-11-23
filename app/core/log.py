import logging
import logging.config
from pathlib import Path


def setup_logger():
    logger_conf_path = Path(__file__).parent / "logger.conf"
    logging.config.fileConfig(logger_conf_path)
