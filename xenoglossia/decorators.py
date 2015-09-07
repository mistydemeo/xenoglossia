from functools import wraps
from importlib import import_module


def string_fn(func):
    @wraps(func)
    def wrapper(input, *args, **kwargs):
        if isinstance(input, list):
            return func(''.join(input), *args, **kwargs)
        else:
            return func(input, *args, **kwargs)
    return wrapper


def array_fn(func):
    @wraps(func)
    def wrapper(input, *args, **kwargs):
        return func(list(input), *args, **kwargs)
    return wrapper


def xenoglossia_fn(func):
    mod = import_module(func.__module__)
    try:
        mod.XG_FUNCTIONS.append(func.__name__)
    except AttributeError:
        mod.XG_FUNCTIONS = [func.__name__]

    return func
