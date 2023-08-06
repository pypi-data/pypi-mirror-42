#!/usr/bin/env python3
"""
Simple pipeline json parser

It is as jq but better because you can use python syntax and you do not need
to look in documentation every time.
"""

import json
import sys

from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import JsonLexer

__version__ = '1.0.1'


def process(it):
    if len(sys.argv) < 2:
        dump = json.dumps(it, sort_keys=True, indent=4)
        output = highlight(dump, JsonLexer(), TerminalFormatter())
        print(output, end='')
        return

    globs = globals()
    locs = locals()
    print(
        highlight(
            json.dumps(
                eval(sys.argv[1], globs, locs),
                sort_keys=True,
                indent=4
            ),
            JsonLexer(),
            TerminalFormatter()
        ),
        end=''
    )


def main():
    # hack to pass it inside of eval when used in comprehension
    global it
    try:
        stdin = sys.stdin.read()
        it = json.loads(stdin)
        process(it)
    except json.decoder.JSONDecodeError:
        its = [json.loads(line.strip())
               for line in stdin.split('\n') if line.strip()]
        for it in its:
            process(it)


if __name__ == '__main__':
    main()
