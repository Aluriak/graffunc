"""
Definition of the main class of the API, ConvertionSpreader.

"""
import itertools
from collections import defaultdict

from . import validator
from . import solving
from graffunc import path_walk, path_search


class graffunc:
    """Defines an API for build and solve a network of functions.

    """

    def __init__(self, paths_dict=None):
        """Expect a dict {{sources}: {{targets}: {converter function}}}"""
        self._paths_dict = defaultdict(lambda: defaultdict(set), {
            frozenset(preds): defaultdict(set, {frozenset(succs): {func}
                                                for succs, func in sub.items()})
            for preds, sub in (paths_dict or {}).items()
        })
        self.validate()


    def validate(self):
        """Perform analysis of internal data. Raise ValueError on error."""
        validator.validate_paths_dict(self.paths_dict)
        if not validator.is_valid_paths_dict(self.paths_dict):
            raise ValueError("validator.is_valid_paths_dict does not consider "
                             "given paths_dict to be valid: " + str(self._paths_dict))

    def add(self, func:callable, sources:iter, targets:iter):
        """Add given func as converter from source to target"""
        sources, targets = frozenset(sources), frozenset(targets)
        self._paths_dict[sources][targets].add(func)
        self.validate()

    def convert(self, sources:dict, targets:iter, search=path_search.greedy) -> dict:
        """Return the same data, once converted to target from source"""
        return path_walk.applied(self._paths_dict, dict(sources),
                                 frozenset(targets), search=search)

    def reachables(self, sources:iter) -> iter((callable, type)):
        """Return the types reachable and used function
        if given sources are available.

        """
        yield from path_walk.theoric_exploration(
            self._paths_dict, frozenset(sources)
        )

    def reachables_types(self, sources:iter, include_sources:bool=True) -> frozenset:
        """Return the types reachable if given sources are available.

        include_sources -- sources types are also returned

        """
        sources = frozenset(sources)
        return frozenset(itertools.chain.from_iterable(
            types for _, types in self.reachables(sources)
        )) | sources if include_sources else {}

    def path(self, data, source, target) -> iter:
        """Yield the functions"""
        raise NotImplementedError()

    @property
    def paths_dict(self) -> dict:
        return dict({ss: dict(sub) for ss, sub in self._paths_dict.items()})
