# Brainlove
Backwards compatible Brainfuck extension. Currently supports Macros (Functions) using horribly annoying syntax, as to keep with the spirit of brainfuck. The interpreter handles both Brainfuck and Brainlove files.

:speech_balloon: This project is not optimized, condensed or follows any proper styleguide - it doesn't matter, it's a one-off project meant as a joke.

## Syntax
As with normal Brainfuck files, the operations:
`< > + - , . [ ]` are all supported.

to utilize the macro-feature of Brainlove, the following syntax must be used:

- `ł` - marks the start of a macro, this should be followed by any `[a-Z]+[a-zA-Z0-9]*` identifier.

- `%` - marks the end of said identifier

- `#` - marks the end of the code the macro contains

- `ŋmyfunctionNameð` here shows that to call a macro, one must prefix and suffix the function identifier with `ŋ` and `ð` respectively


Nested macros _are_ supported, meaning that this definition would be a valid macro:
```brainfuck
łsub10%----------#

łsub30%
ŋsub10ð
ŋsub10ð
ŋsub10ð
#
```

## Usage
```
python3 interpreter.py [sourcefile]
```
## Examples
The [examples/](https://github.com/frederikgram/brainlove/tree/master/examples) directory contains a few examples of both brainlove and brainfuck applications,
examples of the extended languages features are showcased in the former.

