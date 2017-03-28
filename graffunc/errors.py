class InconvertibleError(Exception):
    """Raised when a converter can't convert input data to output format.
    Note that this exception is not a ValueError or TypeError,
    that are raised on unexpected input data.

    """

    pass


class NoPathFound(Exception):
    """Raised when a path search can't found any way to a given target.

    """

    pass

