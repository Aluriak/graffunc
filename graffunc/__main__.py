"""
Usage example of the module.

Refer to unit tests for further examples.

"""

from graffunc import graffunc, InconvertibleError


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


assert {'a', 'b', 'c'} == grfc.reachables_types(sources={'a'})
assert {'b', 'c'} == grfc.reachables_types(sources={'b'})
assert {'c'} == grfc.reachables_types(sources={'c'})

assert {'b': 'HELLO'} == grfc.convert(sources={'a': 'hello'}, targets={'b'})
assert {'c': 'payload: HELLO/payload'} == grfc.convert(sources={'a': 'hello'}, targets={'c'})
