"""
    From an idea of https://gist.github.com/nguyenkims hosted on: https://gist.github.com/nguyenkims/e92df0f8bd49973f0c94bddf36ed7fd0
"""
import logging
import sys
from logging.handlers import  RotatingFileHandler

FORMATTER = None
LOG_FILE = None
LEVEL = logging.DEBUG
PROPAGATE = True

# RotatingFileHandler properties
MAX_BYTES = 5000000 # 5MB
BACKUP_COUNT = 5

_loggers_cache = {}

def _get_console_handler():
	console_handler = logging.StreamHandler(sys.stdout)
	console_handler.setFormatter(FORMATTER)
	return console_handler

def _get_file_handler():
	file_handler = RotatingFileHandler(LOG_FILE, backupCount=BACKUP_COUNT, maxBytes=MAX_BYTES)
	file_handler.setFormatter(FORMATTER)
	return file_handler

def get_logger(logger_name) -> logging.Logger:
    if logger_name not in _loggers_cache:
        logger = logging.getLogger(logger_name)

        logger.setLevel(LEVEL) # better to have too much log than not enough

        logger.addHandler(_get_console_handler())

        if LOG_FILE is not None:
            logger.addHandler(_get_file_handler())

        # with this pattern, it'zs rarely necessary to propagate the error up to parent
        logger.propagate = PROPAGATE

        #
        _loggers_cache[logger_name] = logger
    else:
        logger = _loggers_cache[logger_name]
    
    return logger