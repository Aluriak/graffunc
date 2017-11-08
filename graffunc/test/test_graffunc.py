

import pytest
from graffunc import graffunc, InconvertibleError, path_walk


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
    def my_ad_to_ef_converter(a, d):
        return {'e': d.join(a), 'f': a.join(d)}
    def my_gh_to_i_converter(arg:'g', *, kwonly:'h'):
        return {'i': arg + kwonly}

    # creation of the main object
    grfc = graffunc({
        ('a',): {('b',): my_a_to_b_converter},
        ('a', 'd'): {('e', 'f'): my_ad_to_ef_converter},
        ('g', 'h'): {('i',): my_gh_to_i_converter},
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

def test_graffunc_api_convert_3(grfc):
    expected = {'e': '..'.join('hello'), 'f': '.hello.'}
    assert expected == grfc.convert(sources={'a': 'hello', 'd': '..'}, targets={'e', 'f'})

def test_graffunc_api_convert_4(grfc):
    expected = {'i': 'helloworld'}
    assert expected == grfc.convert(sources={'g': 'hello', 'h': 'world'}, targets={'i'})


def test_graffunc_api_reachable_a(grfc):
    assert {'a', 'b', 'c'} == grfc.reachables_types(sources={'a'})

def test_graffunc_api_reachable_b(grfc):
    assert {'b', 'c'} == grfc.reachables_types(sources={'b'})

def test_graffunc_api_reachable_c(grfc):
    assert {'c'} == grfc.reachables_types(sources={'c'})


def test_graffunc_api_reachable_ad(grfc):
    assert {'a', 'b', 'c', 'd', 'e', 'f'} == grfc.reachables_types(sources={'a', 'd'})
