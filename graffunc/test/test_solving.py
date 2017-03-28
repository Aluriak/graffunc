"""
Unit tests about the solving module.

"""

import unittest

from graffunc import solving


class TestGraffuncWidely(unittest.TestCase):

    @unittest.skip("These tests needs to be rewritten")
    def test_chain(self):
        self.assert_paths(
            graph={1: {2}, 2: {3}, 3: {4}, 4: {5}},
            paths={
                (1, 1): (),
                (1, 2): (1, 2),
                (1, 3): (1, 2, 3),
                (1, 4): (1, 2, 3, 4),
                (1, 5): (1, 2, 3, 4, 5),
                (1, 6): None,
            }
        )

    @unittest.skip("These tests needs to be rewritten")
    def test_big_graph(self):
        self.assert_paths(
            graph={
                1: {2, 3, 4, 5},
                3: {2, 5},
                5: {6, 2},
            },
            paths={
                (1, 1): (),
                (1, 2): (1, 2),
                (1, 6): (1, 5, 6),
                (3, 5): (3, 5),
            }
        )

    def assert_paths(self, graph, paths):
        for (source, target), expected_path in paths.items():
            with self.subTest(source=source, target=target):
                self.assertEqual(
                    solving.shortest_path(graph, source, target),
                    expected_path
                )
