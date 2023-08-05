"""
Utils for lamapi.
"""


class _NoValue(object):
    """
    Represent for no value.
    """

    def __repr__(self):
        return 'no value'

    def __reduce__(self):
        return '_novalue'


_no_value = _NoValue()


class cached_property(property):
    """
    A decorator that converts a function into a lazy property.  The
    function wrapped is called the first time to retrieve the result
    and then that calculated result is used the next time you access
    the value::
        class Foo(object):
            @cached_property
            def foo(self):
                # calculate something important here
                return 42
    The class has to have a `__dict__` in order for this property to
    work.
    From pallets/werkzeug.
    """

    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func

    def __set__(self, obj, value):
        obj.__dict__[self.__name__] = value

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__, _NoValue)
        if value is _NoValue:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value
        return value
