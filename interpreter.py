""" Brain(fuck|love) interpreter """

import sys
from collections import defaultdict
from typing import *


# [Label Name: Index in token list]
labels: Dict[str, int] = defaultdict(None)

# [Macro Name: List of operations]
macros: Dict[str, List[str]] = defaultdict(list)

# Blacklisted characters, instead of stripping
# the source file, we skip over them as to
# keep the original position in the file for
# debugging / logging purposes
ignores: List[str] = ['\n', ' ', ':', '']

# Valid Brain(fuck/love) operations
operations: List[str] = ["<", ">", "+", "-", ".", ",", "[", "]"]

# Macro-specific operations
macro_operations: List[str] = ['ł','%','#','ŋ', 'ð']


def preprocessor(source: str) -> List[str]:
    """Given a source input, convert it to a
    list of valid Brainlove tokens, filling in
    macro definitions automatically
    """

    tokens: List[str] = list()

    def eat(cursor, delim) -> Tuple[int, str]:
        buffer: str = ""

        while (c := source[cursor]) != delim:
            buffer += c
            cursor += 1

        return cursor + 1, buffer

    def eat_macro_name(cursor) -> Tuple[int, str]:
        buffer: str = ""
        while (
            source[cursor] not in ignores
            and source[cursor] not in operations
            and source[cursor] != "ð"
        ):

            buffer += source[cursor]
            cursor += 1

        return cursor, buffer

    cursor: int = 0
    while cursor < len(source):

        # Start of macro definition
        if source[cursor] == "ł":
            cursor, macro_name = eat(cursor + 1, "%")

            # Store the body of the macro
            while source[cursor] != "#":
                if source[cursor] in ignores:
                    cursor += 1

                elif source[cursor] == "ł":
                    print(
                        "Invalid Macro Body: Cannot put a macro-definition inside of the body of another macro, position: ",
                        cursor,
                    )
                    sys.exit(-1)

                # Nested Macro
                elif source[cursor] == 'ŋ':
                    cursor, nested_macro_name = eat_macro_name(cursor + 1)
                    macros[macro_name].extend(macros[nested_macro_name])

                # Normal Operation
                else:
                    macros[macro_name].append(source[cursor])
                    cursor += 1

        # Macro as Operation
        elif source[cursor] == 'ŋ':
            cursor, macro_name = eat_macro_name(cursor + 1)
            tokens.extend(macros[macro_name])

        # Normal Operation
        if source[cursor] in operations:
            tokens.append(source[cursor])

        cursor += 1

    return tokens


def interpreter(tokens: List[str]) -> DefaultDict[int, int]:
    """Given a list of tokens, simulate the
    actions performed in-memory and return the
    final state of the heap
    """

    heap: Final[Dict[int, int]] = defaultdict(int)
    loop_stack: Final[List[int]] = list()
    pointer: int = 0

    cursor: int = 0
    while cursor < len(tokens):

        # The following if-elif clauses
        # could be either converted into
        # case-matching in later versions of
        # python, or into a dictionary where
        # the value stored is a callable that
        # would mutate a given state
        # but this is for simplicity's sake

        if tokens[cursor] == "[":
            loop_stack.append(cursor)

            if heap[pointer] == 0:
                while (c := tokens[cursor]) != "]":
                    cursor += 1

        elif tokens[cursor] == "]":
            if heap[pointer] != 0:
                cursor = loop_stack.pop() - 1

        elif tokens[cursor] == "<":
            pointer -= 1

        elif tokens[cursor] == ">":
            pointer += 1

        elif tokens[cursor] == "+":
            heap[pointer] += 1

        elif tokens[cursor] == "-":
            heap[pointer] -= 1

        elif tokens[cursor] == ".":
            print(heap[pointer])

        elif tokens[cursor] == ",":
            intake = input(">:  ")
            heap[pointer] = int(intake) if intake.isdigit() else ord(intake)

        cursor += 1

    return heap


if __name__ == "__main__":

    try:
        source = open(sys.argv[1], "r")
    except FileNotFoundError:
        print(f"Brain(fuck|love) source file '{sys.argv[1]}' could not be found")
        sys.exit(-1)

    source = source.read()
    tokens = preprocessor(source)
    heap = interpreter(tokens)
    print(heap)
