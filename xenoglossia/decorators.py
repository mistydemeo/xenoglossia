from functools import wraps
from importlib import import_module


def string_fn(func):
    """
    Converts the `input` argument of the wrapped function into a string, if it is not already.
    Coerces arrays by joining their contents without a separator.
    """
    @wraps(func)
    def wrapper(input, *args, **kwargs):
        if isinstance(input, list):
            return func(''.join(input), *args, **kwargs)
        else:
            return func(input, *args, **kwargs)
    return wrapper


def array_fn(func):
    """
    Converts the `input` argument of the wrapped function into a list, if it is not already.
    Coerces strings by converting them into a list of each individual character.
    """
    @wraps(func)
    def wrapper(input, *args, **kwargs):
        return func(list(input), *args, **kwargs)
    return wrapper


def xenoglossia_fn(func):
    """
    Marks this function as a Xenoglossia function.

    Adds the name of this function to a list named XG_FUNCTIONS in the module in which the wrapped function is defined; if no such list already exists in that namespace, it's created.
    The XG_FUNCTIONS list is used by the module loader to determine which names in a module are intended to be used as Xenoglossia functions.

    This decorator does not actually wrap the function, and returns the original function without modifications.
    """
    mod = import_module(func.__module__)
    try:
        mod.XG_FUNCTIONS.append(func.__name__)
    except AttributeError:
        mod.XG_FUNCTIONS = [func.__name__]

    return func
