"""
Definition of the main class of the API, ConvertionSpreader.

"""
from collections import defaultdict

from . import validator
from . import solving
from . import commons


LOGGER = commons.logger()


class graph:
    """Defines an API for build and solve a network of converters.

    Note that the network is buid each time the convert function is called.
    FrozenConvertionSpreader class is a solution for a quicker version.

    """

    def __init__(self, paths_dict=None):
        """Expect a dict {source: {target: converter function}}"""
        paths_dict = paths_dict if paths_dict else {}
        self._paths_dict = defaultdict(dict, {
            frozenset(sources): {
                frozenset(targets): conv
                for targets, conv in targetsdict.items()
            }
            for sources, targetsdict in paths_dict.items()
        })
        validator.validate_paths_dict(self.paths_dict)
        assert validator.is_valid_paths_dict(self.paths_dict)

    def add(self, inputs, outputs, converter):
        """Add given function as converter from inputs to outputs"""
        inputs, outputs = frozenset(inputs), frozenset(outputs)
        previous_converter = self.paths_dict[inputs].get(outputs, None)
        if previous_converter:
            raise ValueError('A converter ' + str(previous_converter)
                             + ' already exist for inputs ' + str(inputs)
                             + ' and outputs ' + str(outputs) + '.')
        else:
            self.paths_dict[inputs][outputs] = converter

    def convert(self, data, source, target):
        """Return the same data, once converted to target from source"""
        path = solving.windowed_shortest_path(self.paths_dict, source, target)
        for source, target in path:
            data = self.paths_dict[source][target](data)
        return data

    @property
    def paths_dict(self):
        return self._paths_dict

    def exploration(self, start:iter) -> iter:
        """Yield applicable functions"""
        start = frozenset(start)
        found = set(start)
        yielded = set()  # functions already yielded
        terminated = False
        while not terminated:
            terminated = True
            for source, targets in self._paths_dict.items():
                # print('\t\t', source, start, source - start)
                if len(source - found) == 0:
                    for target, converter in targets.items():
                        # filter out already walked cases
                        if converter not in yielded and len(target - found) > 0:
                            found |= target
                            yielded.add(converter)
                            yield converter, target
                            terminated = False
        # print('FOUND:', found)
