import sys
import logging
from wyl import config


def setup_logger():

    logging.basicConfig(
        filename=config.log_filepath,
        filemode="a",
        level=logging.DEBUG,
        encoding="utf-8",
    )

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    return logger
