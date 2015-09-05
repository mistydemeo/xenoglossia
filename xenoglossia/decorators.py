from functools import wraps


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
