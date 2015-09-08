from __future__ import print_function

from argparse import ArgumentParser
import sys

from xenoglossia import NameError, ParseError, run_program

def _parse_args():
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", help="input string", required=False)
    parser.add_argument("command", help="command")
    return parser.parse_args()

def main():
    sucess = 0
    args = _parse_args()
    if not args.input:
        args.input = sys.stdin.read().rstrip("\r\n")

    try:
        result = run_program(args.input, args.command)
    except NameError as e:
        print("Unknown function called: {}".format(e))
        return 65
    except ParseError as e:
        # TODO probably be better not to print pyparsing's error directly
        print("Unable to parse provided program: {}".format(e))
        return 64

    print(result)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
