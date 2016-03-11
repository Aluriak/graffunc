"""
Definition of the main class of the API, ConvertionSpreader.

"""
from collections import defaultdict

from . import validator
from . import solving
from . import commons


LOGGER = commons.logger()


class ConvertionSpreader:
    """Defines an API for build and solve a network of converters.

    Note that the network is buid each time the convert function is called.
    FrozenConvertionSpreader class is a solution for a quicker version.

    """

    def __init__(self, paths_dict=None):
        """Expect a dict {source: {target: converter function}}"""
        paths_dict = paths_dict if paths_dict else {}
        self._paths_dict = defaultdict(dict, paths_dict)
        validator.validate_paths_dict(self.paths_dict)
        assert validator.is_valid_paths_dict(self.paths_dict)
        self._dirty_asp = False

    def add(self, func, source, target):
        """Add given func as converter from source to target"""
        previous_converter = self.paths_dict[source].get(target, None)
        if previous_converter:
            raise ValueError('A converter ' + str(previous_converter)
                             + ' already exist for source ' + str(source)
                             + ' and target ' + str(target) + '.')
        else:
            self.paths_dict[source][target] = func
            self._dirty_asp = True

    def convert(self, data, source, target):
        """Return the same data, once converted to target from source"""
        path = solving.windowed_shortest_path(self.paths_dict, source, target)
        for source, target in path:
            data = self.paths_dict[source][target](data)
        return data

    @property
    def paths_dict(self):
        return self._paths_dict
