"""
Usage:
    knb [-hv] <command> [<args>...]

Options:
    (-h|--help)     show this help
    (-v|--version)  show version

Commands:
    mk - make note
    list - list notes
"""

import sys

import docopt  # type: ignore

from cli.adapters.create_note import create_note_chain
from cli.adapters.list_notes import list_notes_chain
from cli.generator.docopt_generator import Generator

if __name__ == "__main__":

    command_chains = [create_note_chain, list_notes_chain]

    g = Generator()
    commands = g(command_chains)

    args = docopt.docopt(__doc__, version="0.0.1", options_first=True)
    # print(args)
    cmd = args["<command>"]
    command = commands.get(cmd)
    if command is None:
        print("command not found", cmd)
        print(__doc__)
        sys.exit(1)
    command(sys.argv[2:])