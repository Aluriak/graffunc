"""
Various constants definitions.

"""
import logging, logging.config
import pkg_resources  # packaging facilies
import os
from functools   import partial

from .info import PACKAGE_NAME, PACKAGE_VERSION


DIR_ASP_SOURCES = 'asp/'

# Logging constants
LOGGER_NAME       = PACKAGE_NAME
DEFAULT_LOG_LEVEL = logging.DEBUG


# ASP files retrieving
def __asp_file(name):
    "path to given asp source file name"
    return pkg_resources.resource_filename(
        PACKAGE_NAME, DIR_ASP_SOURCES + name + '.lp'
    )
ASP_SRC_FINDPATH = __asp_file('findpath')


# logging functions
def logger(name=LOGGER_NAME):
    """Return logger of given name, without initialize it.

    Equivalent of logging.getLogger() call.

    """
    return logging.getLogger(name)


def configure_logger(term_loglevel=None, loglevel=None):
    """Operate the logger configuration for the package"""
    # use defaults if None given
    term_loglevel = DEFAULT_LOG_LEVEL if term_loglevel is None else term_loglevel
    loglevel = DEFAULT_LOG_LEVEL if loglevel is None else loglevel
    # put given log level in upper case, or keep it as integer
    try:
        loglevel = loglevel.upper()
    except AttributeError:  # loglevel is an integer, not a string
        pass  # nothing to do, lets keep the log level as an int
    try:
        term_loglevel = term_loglevel.upper()
    except AttributeError:  # term_loglevel is an integer, not a string
        pass  # nothing to do, lets keep the log level as an int
    assert isinstance(term_loglevel, int) or isinstance(term_loglevel, str)
    assert isinstance(loglevel, int) or isinstance(loglevel, str)

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
                'level': term_loglevel,
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
        },
        'loggers': {
            PACKAGE_NAME: {
                'handlers':['console'],
                'propagate': True,
                'level': loglevel,
            },
        }
    }

    # apply the configuration
    try:
        # free possible previous configuration
        handlers = logger().handlers[:]
        for handler in handlers:
            handler.close()
            logger().removeHandler(handler)
        logging.config.dictConfig(logging_config)
    except PermissionError:
        logger().warning(os.path.abspath(DIR_LOGS + LOGGER_NAME + '.log')
                        + "can't be written because of a permission error."
                        + "No logs will be saved in file.")


def log_level(level):
    """Set terminal log level to given one"""
    _logger = logger()
    handlers = (_ for _ in _logger.handlers
                if isinstance(_, logging.StreamHandler)
               )
    for handler in handlers:
        handler.setLevel(level.upper())
