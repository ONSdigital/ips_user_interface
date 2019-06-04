import logging.config
from os import path


def __init():
    __logger = logging.getLogger(__name__)
    log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
    logging.config.fileConfig(fname=log_file_path, disable_existing_loggers=False)
    return __logger


log = __init()
