from decorators import string_fn, array_fn, xenoglossia_fn
from random import randrange, shuffle
import re


def _get_arg(args, index, default=None):
    try:
        return args[index]
    except IndexError:
        return default


def _coerce_int(string):
    """
    Coerces `string` into an integer.

    Attempts to parse `string` as an integer.
    If `string` is empty, returns None.
    If `string` cannot be parsed into an integer, returns the sum of the Unicode ordinals of all characters in `string`.
    """
    if not string:
        return
    else:
        try:
            return int(string)
        # cannot parse
        except ValueError:
            return reduce(lambda i, n: i + ord(n), list(string), 0)


@xenoglossia_fn
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


@xenoglossia_fn
def collapse(input, *args):
    """
    args[0]: joiner

    Joins *input* into a single string, with *joiner* in between each substring if provided
    """
    joiner = _get_arg(args, 0, '')
    return joiner.join(input)


@xenoglossia_fn
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


@xenoglossia_fn
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


@xenoglossia_fn
@string_fn
def query(input, *args):
    """
    args[0]: query

    Searches *input* for any occurrences of *query*, and returns the first or, if there is no match, *input*.
    *query* is interpreted as a regular expression.
    """
    query = _get_arg(args, 0, '')

    try:
        match = re.match(query, input)
    except:  # regex doesn't parse
        return input

    if match is not None and match.group():
        return match.group()[0]
    else:
        return input


@xenoglossia_fn
@array_fn
def reject(input, *args):
    """
    args[0]: comparator

    Returns *input* with every occurrence of *comparator* removed.
    """
    comparator = _get_arg(args, 0, '')

    return [el for el in input if el != comparator]


@xenoglossia_fn
@array_fn
def accept(input, *args):
    """
    args[0]: comparator

    Returns *input* with each element which is not *comparator* removed.
    """
    comparator = _get_arg(args, 0, '')

    return [el for el in input if el == comparator]


@xenoglossia_fn
@array_fn
def shuffle(input, *args):
    """
    Randomizes the order of the elements in *input*.
    """
    shuffle(input)
    return input


@xenoglossia_fn
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


@xenoglossia_fn
@array_fn
def interject(input, *args):
    """
    arg[0]: interjection
    arg[1]: index

    Inserts *interjection* into *input* at *index*.
    If *index* is not provided, selects a random index between 0 and the end of *input*.
    If *index* is provided but cannot be parsed into an integer, calculates a value by summing the Unicode codepoint ordinals of all of the characters in *count*.
    """
    interjection = _get_arg(args, 0, '')
    index = _coerce_int(_get_arg(args, 1, ''))
    if index is None:
        index = randrange(0, len(input))

    input.insert(index, interjection)

    return input


@xenoglossia_fn
def arrange(input, *args):
    """
    Arrange all of the elements of *input* in alphabetical order.

    If *input* is a string, returns the string unmodified, because sorting a string results in a boring output.
    """
    if isinstance(input, basestring):
        return input
    else:
        return sorted(input)
