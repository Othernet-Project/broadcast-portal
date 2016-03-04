import functools


class LookupHelper(type):
    """Look up the requested helper function in the registry."""
    def __getattr__(cls, name):
        try:
            return cls.registry[name]
        except KeyError:
            raise AttributeError(name)


class template_helper(object):
    """Decorator for registring and accessing template helper functions.

    Example usage:

    >>> @template_helper
    ... def my_func(a):
    ...     return a
    ...
    >>> my_func(3)
    3
    >>> template_helper.my_func(3)
    3
    >>> template_helper.my_func is my_func
    True
    """
    __metaclass__ = LookupHelper
    registry = dict()

    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)
        self.registry[func.__name__] = self

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
