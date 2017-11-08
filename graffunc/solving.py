"""
Encapsulation of the path search inside dictionnary.

"""
from collections import deque
from itertools import islice

import networkx as nx


def windowed_shortest_path(graph, source, target):
    return windowed(shortest_path(graph, source, target), 2)


def windowed(iterable, size=2):
    """Yields iterms by bunch of a given size, but rolling only one item
    in and out at a time when iterating."""
    iterable = iter(iterable)
    d = deque(islice(iterable, size), size)
    yield d
    for x in iterable:
        d.append(x)
        yield d


def shortest_path(graph, source, target):
    """Return the windowed shortest path between source and target
    in the given graph.

    Graph is expected to be a dict {node: {successors}}.

    Return value is a tuple of 2-tuple, each 2-tuple representing a
    window of size 2 on the path.

    """
    if source == target: return tuple()  # no move needed
    nxg = nx.Graph()
    for node, succs in graph.items():
        for succ in succs:
            nxg.add_edge(node, succ)
    return tuple(nx.dijkstra_path(nxg, source, target))
