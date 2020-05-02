"""
Make note command. create not with summary and content.
If content not providen, you can write it until press Enter
3 times.
Usage:
    mk <SUMMARY> [CONTENT]
"""

from docopt import docopt
import sys


def main(argv):
    args = docopt(__doc__, argv=argv)
    print(args)
    summary = args["<SUMMARY>"]
    content = args["CONTENT"]
    if content is None or len(content) == 0:
        content = ""
        enter_times = 0
        while enter_times < 3:
            line = input("note>")
            if line == "":
                enter_times += 1
            else:
                enter_times = 0
                content += line + "\n"
    # TODO: call usecase to create note


if __name__ == "__main__":
    main(sys.argv)
