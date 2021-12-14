""" Brainfuck interpreter """

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
operations: List[str] = ['<', '>', '+', '-', '.', ',', '[', ']']


def lexer(source: str) -> List[str]:
    """ Given a source input, convert it to a 
    list of valid Brainlove tokens, filling in
    macro definitions automatically """

    tokens: List[str] = list()

    def eat(index, delim) -> Tuple[int, str]:
        buffer: str = ""
    
        while((c := source[index]) != delim):
            buffer += c
            index += 1
    
        return index, buffer

    def eat_macro_name(index) -> Tuple[int, str]:
        buffer: str = ""
        while(True):
            if source[index] in ignores + operations:
                break
    
            buffer += source[index]
            index += 1

        return index, buffer

    cursor: int = 0
    while (cursor < len(source)):

        if cursor + 5 < len(source) and source[cursor:cursor + 5] == 'macro':
            cursor, macro_name = eat(cursor + 6, ':')
            
            while(cursor < len(source) and (c := source[cursor]) != 'e'):
                if c not in ignores:
                    macros[macro_name].append(c)
                cursor += 1

            # Skip over "end:"
            cursor += 4

        elif source[cursor] not in operations:  
            cursor, macro_name = eat_macro_name(cursor)
            tokens.extend(macros[macro_name])
            
        elif source[cursor] in operations:
            tokens.append(source[cursor])

        cursor += 1

    return tokens

def interpreter(tokens: List[str]) -> DefaultDict[int, int]:
    """ Given a list of tokens, simulate the
    actions performed in-memory and return the
    final state of the heap
     """

    heap: Final[Dict[int, int]] = defaultdict(int)
    loop_stack: Final[List[int]] = list()
    pointer: int = 0

    index: int = 0
    while index < len(tokens):
    
        if tokens[index] == '[':    
            loop_stack.append(index)
        
            if heap[pointer] == 0:
                while ((c := tokens[index]) != ']'): index += 1

        elif tokens[index] == ']':
            if heap[pointer] != 0:
                index = loop_stack.pop() - 1

        elif tokens[index] == '<':
            pointer -= 1

        elif tokens[index] == '>':
            pointer += 1

        elif tokens[index] == '+':
            heap[pointer] += 1

        elif tokens[index] == '-':
            heap[pointer] -= 1

        elif tokens[index] == '.':
            print(heap[pointer])

        elif tokens[index] == ',':
            heap[pointer] = int(input(">:"))
    
        index += 1
    
    return heap

if __name__ == "__main__":
    
    try:
        source = open(sys.argv[1], 'r')
    except FileNotFoundError:
        print(f"Brainfuck source file '{sys.argv[1]}' could not be found")
        sys.exit(-1)
    
    source = source.read()
    tokens = lexer(source)
    heap = interpreter(tokens)


