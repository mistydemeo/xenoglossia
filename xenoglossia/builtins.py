# encoding: utf-8
from __future__ import absolute_import

from .decorators import string_fn, array_fn, xenoglossia_fn
from random import randrange, shuffle, randint
import re
from string import ascii_uppercase

from six import b, string_types
from six.moves import range, reduce


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
def transubstantiate(input, *args):
    """
    args[0]: pattern
    args[1]: replacement

    Searches *input* for *pattern*, which is a regular expression, and replaces the first occurrence with *replacement*.
    """
    pattern = _get_arg(args, 0, '')
    replacement = _get_arg(args, 1, '')
    try:
        return re.sub(pattern, replacement, input, count=1)
    except:  # regex doesn't parse
        return input


@xenoglossia_fn
@string_fn
def transubstantiate_all(input, *args):
    """
    args[0]: pattern
    args[1]: replacement

    Searches *input* for *pattern*, which is a regular expression, and replaces all occurrences with *replacement*.
    """
    pattern = _get_arg(args, 0, '')
    replacement = _get_arg(args, 1, '')
    try:
        return re.sub(pattern, replacement, input)
    except:  # regex doesn't parse
        return input


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
@string_fn
def title(input, *args):
    """
    Capitalizes *input* as a title: capitalizes the first letter in every word, with other characters rendered in lowercase.
    """
    return input.title()


# Next three variables for use by the flip function
_FROM_FLIP_CHARS = u" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ?\u203D"
_TO_FLIP_CHARS = u" \u0250q\u0254p\u01DD\u025F\u0183\u0265\u1D09\u027E\u029El\u026Fuodb\u0279s\u0287n\u028C\u028Dx\u028Ez\u2200\u15fa\u0186p\u018E\u2132\u05E4HI\u017F\u029E\u02E5WNO\u0500Q\u0279S\u2534\u2229\u039BMX\u2144Z\u00bf\u2e18"
_FLIP_CHAR_DICT = dict(zip(_FROM_FLIP_CHARS, _TO_FLIP_CHARS))


@xenoglossia_fn
@string_fn
def flip(input, *args):
    """
    Returns an upside down version of *input* prepended by our favorite Flip Table dude.
    """
    char_list = []
    pair = None
    for c in input[::-1]:
        if ord(c) in range(0xDC00, 0xE000):
            # Low part of surrogate pair.  (Comes first because it's reversed.)
            # wikipedia.org/wiki/Universal_Character_Set_characters#Surrogates
            pair = c
        elif ord(c) in range(0xD800, 0xDC00):
            # High part of surrogate pair.
            char_list.append(c)
            char_list.append(pair)
            pair = None
        else:
            char_list.append(c)

    flipped_input = "".join(_FLIP_CHAR_DICT.get(c, c) for c in char_list)
    return u"\uFF08\u256F\u00B0\u25A1\u00B0\uFF09\u256F\uFE35 " + flipped_input


def generate_char_map(start_code):
    """
    Generates a dictionary mapping capitals A through Z with
    the set of Unicode characters starting at start_code.
    """
    char_list = map(lambda i: b("\\U%08x" % (i + start_code)).decode('unicode-escape'), range(0, 25))
    return dict(zip(ascii_uppercase, char_list))

_STARTING_CODES = [119860,  # capital italic
                   120016,  # capital bold script
                   120042,  # lowercase bold script
                   120094,  # lowercase Fraktur small
                   120146,  # lowercase double-struck𝔞
                   120172,  # capital Fraktur
                   120198,  # lowercase Fraktur
                   120224,  # capital sans serif
                   120250,  # lowercase sans serif
                   120276,  # capital bold sans serif
                   120302,  # lowercase bold sans serif
                   120328,  # capital sans serif italic
                   120354,  # lowercase sans serif italic
                   120380,  # capital bold italic
                   120458]  # lowercase monospaced
_CHAR_MAPS = [generate_char_map(sc) for sc in _STARTING_CODES]


@xenoglossia_fn
@string_fn
def ransomize(input, *args):
    """
    Replaces each character of *input* with its companion character from a random code point.
    """
    return "".join(map(lambda c: _CHAR_MAPS[randint(0, len(_CHAR_MAPS) - 1)].get(c, c), input.upper()))


@xenoglossia_fn
@string_fn
def buttify(input, *args):
    """
    Replaces each occurrence of but or butt with the butt emoji. (And no... it's not the peach emoji.)
    """
    return re.sub("(?i)(butt|but)", u"\U0001F351", input)

_DOTMATRIX_CHARS = [u"\u286E\u28b5",
                    u"\u28df\u28F3",
                    u"\u288e\u28c9",
                    u"\u28cf\u2871",
                    u"\u28df\u28cb",
                    u"\u286f\u280d",
                    u"\u288e\u28e5",
                    u"\u2857\u28ba",
                    u"\u2847",
                    u"\u28c9\u280f",
                    u"\u2867\u288e",
                    u"\u28c7\u28c0",
                    u"\u2857\u28ba",
                    u"\u2857\u28bc",
                    u"\u288e\u2871",
                    u"\u286f\u2815",
                    u"\u288e\u28f5",
                    u"\u286f\u2895",
                    u"\u28da\u286b",
                    u"\u28b9\u284f",
                    u"\u2887\u2878",
                    u"\u28a3\u285c",
                    u"\u2867\u28bc",
                    u"\u2871\u288e",
                    u"\u28b1\u284e",
                    u"\u28e9\u28cb"]

_DOTMATRIX_CHAR_DICT = dict(zip(ascii_uppercase, _DOTMATRIX_CHARS))


@xenoglossia_fn
@string_fn
def dotmatrix(input, *args):
    """
    Converts *input* into dot matrix printer format.
    (NOTA BENE: this code has not been tested on an actual dot matrix printer.)
    """
    return "".join(map(lambda c: _DOTMATRIX_CHAR_DICT.get(c, c), input.upper()))


@xenoglossia_fn
@string_fn
def part_title(input, *args):
    """
    Capitalizes the first letter of *input*, and renders all other characters in lowercase.
    """
    return input.capitalize()


@xenoglossia_fn
@string_fn
def shout(input, *args):
    """
    Converts every character of *input* to uppercase.
    """
    return input.upper()


@xenoglossia_fn
@string_fn
def whisper(input, *args):
    """
    Converts every character of *input* to lowercase.
    """
    return input.lower()


@xenoglossia_fn
@string_fn
def illuminate(input, *args):
    """
    Renders the first character in *input* as a Fraktur capital letter, and all other characters as lower case.

    If the first character is not a character in the range of A to Z, leaves it unchanged.
    """
    try:
        firstchr = input[0].lower()
    except IndexError:  # empty string
        return input

    i = ord(firstchr)
    if i in range(97, 122):
        # unichr() won't work for narrow Python builds
        illuminated = b("\\U%08x" % (i - 97 + 120068)).decode('unicode-escape')
        return illuminated + input[1:].lower()
    else:
        return input[0] + input[1:].lower()


@xenoglossia_fn
@string_fn
def flirt(input, *args):
    """
    Converts every character of *input* to full-width.
    """

    char_map = {i: b("\\U%08x" % (i - 33 + 65281)).decode('unicode-escape') for i in range(33, 127)}
    # don't forget the ideographic space character! it's important!
    char_map[32] = b("\\U%08x" % 12288).decode('unicode-escape')

    return ''.join([char_map.get(ord(c), c) for c in input])


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
    for _ in range(0, randrange(1, 10)):
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
    if isinstance(input, string_types):
        return input
    else:
        return sorted(input)
