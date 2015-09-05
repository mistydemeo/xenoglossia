from decorators import string_fn, array_fn


def _get_arg(args, index, default=None):
    try:
        return args[index]
    except IndexError:
        return default


@string_fn
def burst(input, *args):
    separator = _get_arg(args, 0)
    if separator is None:
        return list(input)
    else:
        return input.split(separator)


def collapse(input, *args):
    joiner = _get_arg(args, 0, '')
    return joiner.join(input)


@string_fn
def sub(input, *args):
    original = _get_arg(args, 0, '')
    replacement = _get_arg(args, 1, '')

    return input.replace(original, replacement, 1)


@string_fn
def gsub(input, *args):
    original = _get_arg(args, 0, '')
    replacement = _get_arg(args, 1, '')

    return input.replace(original, replacement)


@array_fn
def reject(input, *args):
    comparator = _get_arg(args, 0, '')

    return [el for el in input if el != comparator]


@array_fn
def accept(input, *args):
    comparator = _get_arg(args, 0, '')

    return [el for el in input if el == comparator]
