"""
Usage:
    knb <command> [<args>...] [options]

Commands:
    mk - make note
    list - list notes
"""

import sys

import docopt  # type: ignore

from cli.adapters.create_note import create_note_chain
from cli.adapters.list_notes import list_notes_chain
from cli.docopt_generator import Generator

if __name__ == "__main__":
    links = [
        create_note_chain,
        list_notes_chain
    ]
    g = Generator()
    commands = g(links)

    args = docopt.docopt(__doc__)
    print(args)
    cmd = args["<command>"]
    command = commands.get(cmd)
    if command is None:
        print("command not found", cmd)
        print(__doc__)
        sys.exit(1)
    command(sys.argv[2:])
