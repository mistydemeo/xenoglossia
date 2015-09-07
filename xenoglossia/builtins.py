from decorators import string_fn, array_fn
from random import randrange, shuffle


def _get_arg(args, index, default=None):
    try:
        return args[index]
    except IndexError:
        return default


@string_fn
def burst(input, *args):
    """
    args[0]: separator

    Splits *input* into an array of substrings, using *separator* as the separator if provided.
    """
    separator = _get_arg(args, 0)
    if separator is None:
        return list(input)
    else:
        return input.split(separator)


def collapse(input, *args):
    """
    args[0]: joiner

    Joins *input* into a single string, with *joiner* in between each substring if provided
    """
    joiner = _get_arg(args, 0, '')
    return joiner.join(input)


@string_fn
def sub(input, *args):
    """
    args[0]: original
    args[1]: replacement

    Replaces the first occurrence of *original* in *input* with *replacement*.
    """
    original = _get_arg(args, 0, '')
    replacement = _get_arg(args, 1, '')

    return input.replace(original, replacement, 1)


@string_fn
def gsub(input, *args):
    """
    args[0]: original
    args[1]: replacement

    Replaces every first occurrence of *original* in *input* with *replacement*.
    """
    original = _get_arg(args, 0, '')
    replacement = _get_arg(args, 1, '')

    return input.replace(original, replacement)


@array_fn
def reject(input, *args):
    """
    args[0]: comparator

    Returns *input* with every occurrence of *comparator* removed.
    """
    comparator = _get_arg(args, 0, '')

    return [el for el in input if el != comparator]


@array_fn
def accept(input, *args):
    """
    args[0]: comparator

    Returns *input* with each element which is not *comparator* removed.
    """
    comparator = _get_arg(args, 0, '')

    return [el for el in input if el == comparator]


@array_fn
def shuffle(input, *args):
    """
    Randomizes the order of the elements in *input*.
    """
    shuffle(input)
    return input


@array_fn
def juggle(input, *args):
    """
    Cycles the elements in *input* to the right a random number of times.

    For example:

    ["1", "2", "3", "4", "5"] => ["3", "4", "5", "1", "2"]
    """
    for _ in xrange(0, randrange(1, 10)):
        input.insert(0, input.pop())

    return input
