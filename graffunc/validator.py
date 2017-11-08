"""
Implementation of various validator of various data.

Validators takes particular data as parameter, and raise ValueError
as soon as an unexpected value is found.

"""
import inspect
from . import commons


def validate_paths_dict(paths_dict):
    """Raise ValueError if given dict is not a {string: {string: callable(1)}}
    where data is valid"""
    [validate_identifier_set(key) for key in paths_dict]
    [validate_identifier_set(key) for subdict in paths_dict.values()
                                  for key in subdict]
    [validate_callable_set(func)  for subdict in paths_dict.values()
                                  for func in subdict.values()]

def positional_parameter_count(func):
    """Return the number of positional parameters that have no default values"""
    sig = inspect.signature(func)
    return len([param for param in sig.parameters.values()
                if param.kind == param.POSITIONAL_OR_KEYWORD
                and param.default is param.empty])

def validate_callable_set(functions:set):
    [validate_callable(func) for func in functions]

def validate_callable(func):
    nb_args = positional_parameter_count(func)
    if not callable(func):
        raise ValueError(func.__name__ + " is not a callable, but a {}."
                         "".format(type(func)))
    if nb_args == 0:
        raise ValueError("Callable " + func.__name__
                         + "takes exactly 0 parameter.")

def validate_identifier_set(ids:frozenset):
    if isinstance(ids, frozenset):
        for idt in ids:
            validate_identifier(idt)
    else:
        raise ValueError("Predecessors and Successors must be wrapped in a frozenset.")

def validate_identifier(idt):
    if not isinstance(idt, str):
        raise ValueError('Identifier ' + str(idt) + ' is not a string.')

def is_valid_template(validator, obj_name):
    """Return a function returning True if validator don't rise any Exception
    when receiving the input parameter"""
    def wrapped(obj):
        """True if given """ + obj_name + """ is valid"""
        try:
            validator(obj)
            return True
        except ValueError:
            return False
        return False
    return wrapped



# Generate the is_valid_object predicates for each validate_object routine.
FUNCS = (func for func in tuple(globals().values())
         if callable(func) and func.__name__.startswith('validate_'))

for validate_func in FUNCS:
    validate_object = validate_func.__name__[len('validate_'):]
    isvalid_func_name = 'is_valid_' + validate_object
    globals()[isvalid_func_name] = is_valid_template(validate_func, validate_object)

del FUNCS
