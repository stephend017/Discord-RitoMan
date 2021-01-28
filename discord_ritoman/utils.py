import datetime
import logging
from logging.handlers import RotatingFileHandler


epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


def create_logger(path: str) -> logging.Logger:
    """
    Creates a logger for a given file path

    Note: `path` should be `__file__` in most cases

    Args:
        path (str): the path of the file (should be `__file__`)

    Returns:
        logging.Logger: The logger created for the given file
    """
    logger = logging.getLogger(path)
    log_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(filename)s:%(funcName)s(%(lineno)d)]: %(message)s"
    )

    my_handler = RotatingFileHandler(
        f"{path}.log",
        mode="a",
        maxBytes=5 * 1024 * 1024,
        backupCount=2,
        encoding=None,
        delay=0,
    )
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)

    logger.setLevel(logging.INFO)
    logger.addHandler(my_handler)

    return logger
