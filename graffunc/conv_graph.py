"""Functions related to the conversion graph manipulation.

"""


import itertools


def flatted_conversions(conv_graph:dict) -> iter:
    """Yield 3-uplet (predecessors, successors, conversion function)"""
    for preds, succ_map in conv_graph.items():
        for succs, funcs in succ_map.items():
            for func in funcs:
                yield preds, succs, func


def conversion_functions(conv_graph:dict) -> iter:
    """Yield all functions found in given conversion graph"""
    yield from itertools.chain.from_iterable(
        funcs
        for target_map in conv_graph.values()
        for funcs in target_map.values()
    )


def seeds(conv_graph:dict) -> iter:
    """Yield all seeds of given graph"""
    yield from itertools.chain.from_iterable(conv_graph.keys())


def all_types(conv_graph:dict) -> iter:
    """Yield all types found in given graph"""
    for preds, succ_map in conv_graph.items():
        yield from preds
        yield from itertools.chain.from_iterable(succ_map.keys())
