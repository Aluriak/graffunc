"""
Various constants definitions.

"""
import pkg_resources  # packaging facilies
from functools import partial, wraps

from .info import PACKAGE_NAME, PACKAGE_VERSION
from .logger import logger


DIR_ASP_SOURCES = 'asp/'


# ASP files retrieving
def __asp_file(name):
    "path to given asp source file name"
    return pkg_resources.resource_filename(
        PACKAGE_NAME, DIR_ASP_SOURCES + name + '.lp'
    )
ASP_SRC_FINDPATH = __asp_file('findpath')


