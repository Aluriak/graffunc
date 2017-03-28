"""Implementation of the two possible path walks: those that apply the path
on data, and those that does not.

The path walker is a functions that take source types and target types,
and return True if the targets are reachable with given sources.

The path applyer is a variation that apply in real time the predicted path
on the data, and therefore will return the fully converted data.

"""


from graffunc import path_search, InconvertibleError


def theoric(conv_graph:dict, sources:iter, targets:iter,
            search=path_search.greedy) -> bool:
    """True if targets can be reached by starting from sources in conv_graph."""
    reached = set(sources)
    searcher = search(conv_graph, frozenset(reached), frozenset(targets))
    conversion_succeed = True

    path = next(searcher, None)
    while path:
        preds, succs, converter = path
        assert conv_graph[preds][succs] == converter
        reached |= succs
        if targets.issubset(reached):
            return True
        path = next(searcher, None)
    return False


def applied(conv_graph:dict, sources:dict, targets:iter,
            search=path_search.greedy) -> dict:
    """True if targets can be reached by starting from sources in conv_graph.

    sources -- mapping {type: value}
    targets -- types to search and return
    return -- mapping {type: value} for all types in targets

    """
    data = dict(sources)  # {type: value} for all found data
    searcher = search(conv_graph, frozenset(data), frozenset(targets))
    conversion_succeed = True

    path = next(searcher, None)
    while path:
        preds, succs, converter = path
        assert conv_graph[preds][succs] == converter
        try:
            results = converter(**{type: data[type] for type in preds}).items()
        except InconvertibleError:
            results = ()  # there is no results
        for type, val in results:
            if type in data:  # already generated data
                assert data[type] == val, ("New val {} is not the same as the "
                                           "old {}".format(val, data[type]))
            data[type] = val
        if targets.issubset(data):
            return {t: v for t, v in data.items() if t in targets}

        try:
            # send False to the searcher if the conversion was unsuccesful
            path = searcher.send(bool(results))
        except StopIteration:
            path = None
    return data
