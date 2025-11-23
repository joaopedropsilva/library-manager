import logging
import logging.config
from pathlib import Path
from enum import Enum


_CURRENT_DIR = Path(__file__).parent
_ROOT_DIR = Path(__file__).parent.parent.parent


class _AvailableLevels(Enum):
    debug = logging.DEBUG
    info = logging.INFO
    warning = logging.WARNING
    error = logging.ERROR
    critical = logging.CRITICAL


def setup_logger(override_option: str = ""):
    conf_path = _CURRENT_DIR / "default-logger.conf"
    custom_logger_conf_path = _ROOT_DIR / "logger.conf"

    if custom_logger_conf_path.exists():
        conf_path = custom_logger_conf_path

    logging.config.fileConfig(conf_path)

    if override_option:
        try:
            new_level = _AvailableLevels[override_option].value
        except KeyError:
            raise ValueError(
                f'Invalid log level override option: "{override_option}". '
                f"Available options are: {list(_AvailableLevels.__members__)}"
            )

        root_logger = logging.getLogger()
        root_logger.setLevel(new_level)

        root_logger.debug(f'Loaded logger with "{conf_path}"')
