import datetime
import logging
import importlib
from logging.handlers import RotatingFileHandler
from typing import Any


epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(dt: datetime.datetime) -> float:
    """
    Returns the number of ms since the EPOCH

    Args:
        dt (float): The timestamp to convert in
        seconds. This can be derived from
        `datetime.datetime.now()`

    Returns:
        float: The time in ms since the epoch
    """
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
        delay=False,
    )
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)

    logger.setLevel(logging.INFO)
    logger.addHandler(my_handler)

    return logger


def dynamic_import_class(module_name: str, class_name: str) -> Any:
    """
    Dynamically imports a class from a given module

    Args:
        module_name (str): the module to dynamically load
        class_name (str): the class to dynamically load

    Returns:
        Any: the class from the module specified
    """
    dclass = None
    module = None

    # assert module existss
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        print("module not found: " + module_name)

    # load class from module
    try:
        dclass = getattr(module, class_name)
    except Exception as e:
        print(e)

    return dclass


def get_db_uri(
    db_type: str, user: str, password: str, host: str, port: int, db_name: str
) -> str:
    """
    builds a database uri from the given parameters

    Args:
        db_type (str): the type of database being accessed
        user (str): the name of the user who has access to
            the database on the host machine
        password (str): the password for the user
        host (str): the IP address of the host machine
        port (int): the port to access the DB on
        db_name (str): the name of the database to access

    Returns:
        str: the full db uri
    """
    return f"{db_type}://{user}:{password}@{host}:{port}/{db_name}"


def with_logging(
    func: Any,
    logger: logging.Logger,
    log_message: str = "Function failed",
    default: Any = None,
    **kwargs: Any,
) -> Any:
    """
    Runs a specified function within a try catch block and
    logs an errors.
    """
    try:
        return func(**kwargs)
    except Exception:
        logger.error(log_message)
        return default
