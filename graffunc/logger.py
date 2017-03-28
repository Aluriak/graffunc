"""Operate the logger configuration for the package"""


import os
import logging, logging.config

from .info import PACKAGE_NAME


LOGGER_NAME = PACKAGE_NAME
DIR_LOGS = 'logs/'
LOG_FILE = os.path.abspath(DIR_LOGS + LOGGER_NAME + '.log')
TERM_LOG_LEVEL = logging.DEBUG
TERM_LOG_LEVEL = logging.DEBUG
FILE_LOG_LEVEL = logging.DEBUG


# define the configuration
logging_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': TERM_LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': FILE_LOG_LEVEL,
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': LOG_FILE,
        },
    },
    'loggers': {
        PACKAGE_NAME: {
            'handlers':['console', 'file'],
            'propagate': True,
            'level': min((FILE_LOG_LEVEL, TERM_LOG_LEVEL)),
        },
    }
}

# apply the configuration
try:
    logging.config.dictConfig(logging_config)
except PermissionError:
    logger().warning(LOG_FILE
                    + "can't be written because of a permission error."
                    + "No logs will be saved in file.")
logger = logging.getLogger(PACKAGE_NAME)
