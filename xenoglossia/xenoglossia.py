import builtins

from pyparsing import Group, OneOrMore,  Word, QuotedString, ZeroOrMore, alphas, alphanums

sq_string = QuotedString( quoteChar="'" )
dq_string = QuotedString( quoteChar='"' )
STRING = sq_string ^ dq_string

IDENTIFIER = Word( alphas + "_", alphanums + "_" )

FUNCTION_CALL = Group( IDENTIFIER + ZeroOrMore( STRING ) )

PROGRAM = OneOrMore ( FUNCTION_CALL )


def tokenize(program):
    return [{'function': el[0], 'arguments': el[1:] } for el in PROGRAM.parseString(program)]


def run_program(input, program):
    tokens = tokenize(program)

    for token in tokens:
        func = getattr(builtins, token['function'])
        input = func(input, *token['arguments'])

    if isinstance(input, list):
        input = ''.join(input)

    return input
