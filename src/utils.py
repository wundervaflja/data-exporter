import functools
import logging
import time
from datetime import datetime
# from logging import handlers

import yaml
from definitions import CONFIG_PATH
# from definitions import LOGS_PATH


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    stream = logging.StreamHandler()
    stream.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream.setFormatter(formatter)
    logger.addHandler(stream)
    # Uncomment to have logs stored into the file, create logs dir before
    # fh = handlers.RotatingFileHandler(LOGS_PATH, mode="w+", maxBytes=1e+7, backupCount=10)
    # fh.setLevel(logging.INFO)
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)
    return logger


def exception_logger(logger):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur and suppress it

    @param logger: The logging object
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                logger.exception(err)
                # suppress exception

        return wrapper

    return decorator


def timed(logger):
    """This decorator logs the execution time for the decorated function."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            logger.debug(
                "{} with args {} and kwargs {} ran in {}s".format(func.__name__, args, kwargs, round(end - start, 2)))
            return result

        return wrapper

    return decorator


def value_or_none(value):
    if value == "None":
        return None
    else:
        return value


def convert_unix_ts_to_datetime(unix_ts):
    if not unix_ts:
        return None
    if isinstance(unix_ts, str):
        unix_time, miliseconds = unix_ts.split(".")
        main_time = int(unix_time)
    else:
        main_time = unix_ts
        miliseconds = "0"
    datetime_value = datetime.utcfromtimestamp(main_time).strftime('%Y-%m-%d %H:%M:%S')
    return ".".join([datetime_value, miliseconds])


def get_config(path):
    with open(CONFIG_PATH, 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        parts = path.split(".")
        for part in parts:
            cfg = cfg[part]
        return cfg