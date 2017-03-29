"""Example of graffunc application: inference of orbital property"""

import inspect
from math import sqrt
import graffunc


PHYSIC_GRAVITATIONNAL_CONSTANT = 6.67e-11


def conv_orbital_speed(mass1, mass2, dist, semimajoraxis) -> 'speed':
    """Return orbital speed of a body of mass m1 (kg) orbiting a body
    of mass m2 (kg) at a distance r (meter), and with a semi major axis a.
    The returned speed is in meter per second.
    """
    return sqrt(PHYSIC_GRAVITATIONNAL_CONSTANT * (mass1 + mass2)
                * (1. / dist) - (2. / semimajoraxis))


def conv_speed_from_semimajoraxis_distance(mass1, mass2, semimajoraxis, distance) -> 'speed':
    return sqrt(PHYSIC_GRAVITATIONNAL_CONSTANT * (mass1 + mass2)
                * (2. / distance - 1. / semimajoraxis))

def conv_semimajoraxis_from_speed_distance(mass1, mass2, speed, distance) -> 'semimajoraxis':
    return -1. / (speed * speed / (PHYSIC_GRAVITATIONNAL_CONSTANT
                  * (mass1 + mass2)) - 2. / distance)

def conv_distance_from_speed_semimajoraxis(mass1, mass2, speed, semimajoraxis) -> 'distance':
    return 2. / (speed * speed / (PHYSIC_GRAVITATIONNAL_CONSTANT
                 * (mass1 + mass2)) + 1. / semimajoraxis)


def conv_eccentricity_from_apsis(periapsis, apoapsis) -> 'eccentricity':
    return abs((apoapsis - periapsis) / (apoapsis + periapsis))

def conv_apoapsis_from_eccentricity(eccentricity, periapsis) -> 'apoapsis':
    return (periapsis * (eccentricity + 1)) / (1. - eccentricity)

def conv_periapsis_from_eccentricity(eccentricity, apoapsis) -> 'periapsis':
    return (apoapsis * (1. - eccentricity)) / (eccentricity + 1)


def conv_semimajoraxis_from_periapsis_apoapsis(periapsis, apoapsis) -> 'semimajoraxis':
    return (periapsis + apoapsis) / 2.;

def conv_periapsis_from_semimajoraxis_apoapsis(semimajoraxis, apoapsis) -> 'periapsis':
    return 2. * semimajoraxis - apoapsis;

def conv_apoapsis_from_semimajoraxis_periapsis(semimajoraxis, periapsis) -> 'apoapsis':
    return 2. * semimajoraxis - periapsis;

def conv_periapsis_from_eccentricity_semimajoraxis(eccentricity, semimajoraxis) -> 'periapsis':
    return (1 - eccentricity) * semimajoraxis

def conv_apoapsis_from_eccentricity_semimajoraxis(eccentricity, semimajoraxis) -> 'apoapsis':
    return (1 + eccentricity) * semimajoraxis


def conv_eccentricity_from_semimajoraxis_semiminoraxis(semimajoraxis, semiminoraxis) -> 'eccentricity':
    return sqrt(1. - (semiminoraxis * semiminoraxis) / (semimajoraxis * semimajoraxis))

def conv_semimajoraxis_from_semiminoraxis_eccentricity(semiminoraxis, eccentricity) -> 'semimajoraxis':
    return sqrt((semiminoraxis * semiminoraxis) / (1. - eccentricity * eccentricity))

def conv_semiminoraxis_from_eccentricity_semimajoraxis(eccentricity, semimajoraxis) -> 'semiminoraxis':
    return sqrt((semimajoraxis * semimajoraxis)
                - (semimajoraxis * semimajoraxis)
                * (eccentricity * eccentricity))


def properties(func):
    """Return (args names, (return annotation splitted by comma)) of given func

    >>> def f(a, b) -> 'c,d': pass
    >>> properties(f)
    (('a', 'b'), ('c', 'd'))

    """
    specs = inspect.getfullargspec(func)
    return tuple(specs.args), tuple(specs.annotations['return'].split(','))


def converters():
    """Return an iterable of convertion functions found in global space"""
    return tuple(attr for attr_name, attr in globals().items()
                 if callable(attr) and attr_name.startswith('conv_'))


if __name__ == "__main__":
    graph = graffunc.graffunc()
    for converter in converters():
        arg_types, ret_type = properties(converter)
        graph.add(converter, sources=arg_types, targets=ret_type)

    for start in (('eccentricity', 'distance', 'speed', 'mass1', 'mass2'),
                  ('semimajoraxis', 'speed', 'mass1', 'mass2'),
                  ('eccentricity', 'semimajoraxis')):
        print('STARTING:', start)
        for converter, found in graph.reachables(start):
            print('\t', ', '.join(found).ljust(20), '\t\t(using', converter.__name__ + ')')
        print()
