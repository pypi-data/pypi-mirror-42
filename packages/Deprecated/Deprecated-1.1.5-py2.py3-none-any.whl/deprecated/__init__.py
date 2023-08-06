# -*- coding: utf-8 -*-
"""
Deprecated Library
==================

Python ``@deprecated`` decorator to deprecate old python classes, functions or methods.

"""
import functools
import inspect
import warnings

#: Module Version Number, see `PEP 396 <https://www.python.org/dev/peps/pep-0396/>`_.
__version__ = "1.1.5"

string_types = (type(b''), type(u''))


def deprecated(reason):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.

    **Classic usage:**

    To use this, decorate your deprecated function with **@deprecated** decorator:

    .. code-block:: python

       from deprecated import deprecated


       @deprecated
       def some_old_function(x, y):
           return x + y

    You can also decorate a class or a method:

    .. code-block:: python

       from deprecated import deprecated


       class SomeClass(object):
           @deprecated
           def some_old_method(self, x, y):
               return x + y


       @deprecated
       class SomeOldClass(object):
           pass

    You can give a "reason" message to help the developer to choose another function/class:

    .. code-block:: python

       from deprecated import deprecated


       @deprecated(reason="use another function")
       def some_old_function(x, y):
           return x + y

    :type  reason: str or callable or type
    :param reason: Reason message (or function/class/method to decorate).
    """

    if isinstance(reason, string_types):

        # The @deprecated is used with a 'reason'.
        #
        # .. code-block:: python
        #
        #    @deprecated("please, use another function")
        #    def old_function(x, y):
        #      pass

        def decorator(func1):

            if inspect.isclass(func1):

                fmt1 = "Call to deprecated class {name} ({reason})."
                old_new1 = func1.__new__

                def wrapped_new1(cls, *args, **kwargs):
                    warnings.simplefilter('always', DeprecationWarning)
                    warnings.warn(
                        fmt1.format(name=func1.__name__, reason=reason),
                        category=DeprecationWarning,
                        stacklevel=2
                    )
                    warnings.simplefilter('default', DeprecationWarning)
                    if old_new1 is object.__new__:
                        return old_new1(cls)
                    # actually, we don't know the real signature of *old_new1*
                    return old_new1(*args, **kwargs)

                func1.__new__ = classmethod(wrapped_new1)
                return func1

            elif inspect.isroutine(func1):

                fmt1 = "Call to deprecated function {name} ({reason})."

                @functools.wraps(func1)
                def new_func1(*args, **kwargs):
                    warnings.simplefilter('always', DeprecationWarning)
                    warnings.warn(
                        fmt1.format(name=func1.__name__, reason=reason),
                        category=DeprecationWarning,
                        stacklevel=2
                    )
                    warnings.simplefilter('default', DeprecationWarning)
                    return func1(*args, **kwargs)

                return new_func1

            else:
                raise TypeError(repr(type(func1)))

        return decorator

    elif inspect.isclass(reason):

        cls2 = reason
        fmt2 = "Call to deprecated class {name}."

        old_new2 = cls2.__new__

        def wrapped_new2(cls, *args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(
                fmt2.format(name=cls2.__name__),
                category=DeprecationWarning,
                stacklevel=2
            )
            warnings.simplefilter('default', DeprecationWarning)
            if old_new2 is object.__new__:
                return old_new2(cls)
            # actually, we don't know the real signature of *old_new2*
            return old_new2(*args, **kwargs)

        cls2.__new__ = classmethod(wrapped_new2)
        return cls2

    elif inspect.isroutine(reason):
        # The @deprecated is used without any 'reason'.
        #
        # .. code-block:: python
        #
        #    @deprecated
        #    def old_function(x, y):
        #      pass

        func2 = reason
        fmt2 = "Call to deprecated function {name}."

        @functools.wraps(func2)
        def new_func2(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(
                fmt2.format(name=func2.__name__),
                category=DeprecationWarning,
                stacklevel=2
            )
            warnings.simplefilter('default', DeprecationWarning)
            return func2(*args, **kwargs)

        return new_func2

    else:
        raise TypeError(repr(type(reason)))
