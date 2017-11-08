"""Implementation of various path search.

A path search is basically a generator of path

Functions around there share the following properties:

- coroutine, yielding 3-uplet(predecessor types, successor types, function) to apply on the explorated data.
- expect to receive a False if the sent conversion was not successful.
- take in input the graph, the seeds and the targets.

"""


from graffunc import NoPathFound
from graffunc.conv_graph import flatted_conversions, all_types


def exploration(graph:dict, sources:iter) -> iter:
    """Yield conversion operations to make. Expect to receive an indication
    about conversion success.

    graph -- {{pred types}: {{succ types}: function}} mapping
    sources -- iterable of types available
    yield -- functions to apply on data
    receive -- False if last yielded function does not works

    This implementation is greedy : it will basically try everything until
    nothing seems doable.

    """
    founds = frozenset(sources)
    unused_conversions = set(flatted_conversions(graph))
    if not founds.issubset(frozenset(all_types(graph))):
        print(founds, tuple(all_types(graph)))
        raise ValueError("A source type is not in conversion graph.")
    while unused_conversions:
        for preds, succs, func in unused_conversions:
            if preds.issubset(founds) and not succs.issubset(founds):
                break
        else:  # no possible conversion found
            return frozenset(founds)
        # in all cases, the conversion is not interesting
        unused_conversions.remove((preds, succs, func))
        if (yield preds, succs, func) is False:
            pass  # the conversion failed
        else:  # the conversion succeed
            founds |= succs


def greedy(graph:dict, sources:iter, target_types:iter) -> iter:
    """Yield conversion operations to make. Expect to receive an indication
    about conversion success.

    graph -- {{pred types}: {{succ types}: function}} mapping
    sources -- iterable of types available
    target_types -- iterable of types to get
    yield -- functions to apply on data
    receive -- False if last yielded function does not works

    This implementation is greedy : it will basically try everything
    while targets are not found.

    """
    targets = frozenset(target_types)
    founds = frozenset(sources)
    unused_conversions = set(flatted_conversions(graph))
    if not founds.issubset(frozenset(all_types(graph))):
        raise ValueError("A source type is not in conversion graph.")
    while targets and unused_conversions:
        for preds, succs, func in unused_conversions:
            if preds.issubset(founds) and not succs.issubset(founds):
                break
        else:  # no possible conversion found
            raise NoPathFound("The following targets are not reachable: " + ', '.join(targets))
        # in all cases, the conversion is not interesting
        unused_conversions.remove((preds, succs, func))
        if (yield preds, succs, func) is False:
            pass  # the conversion failed
        else:  # the conversion succeed
            targets -= succs
            founds |= succs
