"""
Various constants definitions.

"""
import inspect
import pkg_resources  # packaging facilies
from functools import partial, wraps

from .info import PACKAGE_NAME, PACKAGE_VERSION


DIR_ASP_SOURCES = 'asp/'


# ASP files retrieving
def __asp_file(name):
    "path to given asp source file name"
    return pkg_resources.resource_filename(
        PACKAGE_NAME, DIR_ASP_SOURCES + name + '.lp'
    )
ASP_SRC_FINDPATH = __asp_file('findpath')


def call_converter(converter:callable, predecessors:dict) -> dict:
    """Return the result obtained by calling the converter with the
    given predecessors {type: value} as input.
    """
    argspec = inspect.getfullargspec(converter)
    all_args = tuple(argspec.args + argspec.kwonlyargs)
    nb_args = len(all_args)

    # if number of (positional) args equals the number of predecessor
    if (nb_args == len(predecessors) == 1) or (len(argspec.args) == len(predecessors) == 1):
        params = {all_args[0]: next(iter(predecessors.values()))}
    else:  # let's use args name
        params = {arg: predecessors[arg] for arg in all_args if arg in predecessors}
        if len(params) < len(predecessors):  # let's use annotations
            # map  predecessor type -> arg, inferred from annotations, minus already matching args
            matching_annotations = {argspec.annotations[arg]: arg for arg in all_args
                                    if argspec.annotations.get(arg) in predecessors
                                    and arg not in params}
            params.update({
                arg: predecessors[pred]
                for pred, arg in matching_annotations.items()
            })
    return converter(**params)
