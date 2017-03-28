

import pytest
from graffunc import graffunc, InconvertibleError, logger, path_walk


@pytest.fixture
def grfc():
    def my_a_to_b_converter(a):
        b = a.upper()
        return {'b': b}
    def my_b_to_c_converter(b):
        c = 'payload: ' + b + '/payload'
        return {'c': c}
    def my_a_to_c_converter(a):
        raise InconvertibleError()

    # creation of the main object
    grfc = graffunc({
        ('a',): {('b',): my_a_to_b_converter},
    })
    # dynamic modification of the object
    grfc.add(my_b_to_c_converter, sources={'b'}, targets={'c'})
    grfc.add(my_a_to_c_converter, sources={'a'}, targets={'c'})

    return grfc


def test_graffunc_path_walk_theoric(grfc):
    assert path_walk.theoric(grfc.paths_dict, {'a'}, {'b'}) is True

def test_graffunc_path_walk_applied(grfc):
    input_data = {'a': 'hello, world'}
    targets = {'b', 'c'}
    expected = {'b': 'HELLO, WORLD', 'c': 'payload: HELLO, WORLD/payload'}
    assert path_walk.applied(grfc.paths_dict, input_data, targets) == expected


def test_graffunc_api_convert_1(grfc):
    expected = {'b': 'HELLO'}
    assert expected == grfc.convert(sources={'a': 'hello'}, targets={'b'})

def test_graffunc_api_convert_2(grfc):
    expected = {'c': 'payload: HELLO/payload'}
    assert expected == grfc.convert(sources={'a': 'hello'}, targets={'c'})
