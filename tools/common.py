import os
from typing import Union
from datetime import datetime
from loguru._logger import Logger

from settings import LOG_DIR

logger: Union[Logger, None] = None


def get_logger():
    global logger
    if logger is None:
        from loguru import logger as log

        logger = log
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

        log_file = os.path.join(LOG_DIR, f'{datetime.now().strftime("%Y%m%d")}.log')
        logger.add(
            log_file,
            rotation="04:00",
            compression="zip",
            level="DEBUG",
        )

    return logger
