"""
Usage example of the module.

Refer to unit tests for further examples.

"""

from graffunc import ConvertionSpreader


def my_a_to_b_converter(a):
    b = a.upper()
    return b
def my_b_to_c_converter(b):
    c = 'payload: ' + b + '/payload'
    return c


# creation of the main object
cp = ConvertionSpreader({
    'a': {'b': my_a_to_b_converter},
})
# dynamic modification of the object
cp.add(my_b_to_c_converter, source='b', target='c')


assert 'DATA' == cp.convert('data', source='a', target='b')
assert 'payload: DATA/payload' == cp.convert('data', source='a', target='c')
