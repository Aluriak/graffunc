
import pytest
from graffunc.conv_graph import flatted_conversions, conversion_functions, seeds


@pytest.fixture
def conv_graph():
    return {(1,): {2: {12}, 3: {13}}, (2,): {1: {21, 212}, 2: {22}}}


def test_flatted(conv_graph):
    expected = {((1,), 2, 12), ((1,), 3, 13), ((2,), 1, 21), ((2,), 1, 212), ((2,), 2, 22)}
    assert set(flatted_conversions(conv_graph)) == expected

def test_conversion(conv_graph):
    expected = {12, 13, 21, 212, 22}
    assert set(conversion_functions(conv_graph)) == expected

def test_seeds(conv_graph):
    expected = {1, 2}
    assert set(seeds(conv_graph)) == expected
