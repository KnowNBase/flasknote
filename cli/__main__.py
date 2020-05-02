"""
Usage:
    knb <COMMAND> [ARGS...] [options]

Commands:
    mk - make note
    list - list notes
"""

import sys

import docopt

from cli import commands as cmds


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    print(args)
    cmd = args["<COMMAND>"]
    command = getattr(cmds, cmd+"_main")
    if not command:
        print("command not found", cmd)
        print(__doc__)
        sys.exit(1)
    command(sys.argv[2:])
