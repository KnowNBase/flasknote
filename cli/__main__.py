"""
Usage:
    knb <command> [<args>...] [options]

Commands:
    mk - make note
    list - list notes
"""

import sys
import typing as t

# noinspection Mypy
import docopt

from cli.docopt_generator import Generator
from cli.generator import Chain
from domain.use_cases.create_note import UseCase
from storage.gateways.create_note_gateway import DictCreateNoteGateway


def input_parser(args: t.Dict[str, t.Any]) -> UseCase.Input:
    summary = args["<summary>"]
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
    return UseCase.Input("1", summary, content)


def output_presentor(output: UseCase.Output):
    if output.errors:
        for e in output.errors:
            print("ERROR:", e)
    else:
        print(f"note '{output.note}' created")


if __name__ == "__main__":
    links = [
        Chain(
            usecase=UseCase,
            dependencies=dict(gateway=DictCreateNoteGateway()),
            command_name="mk",
            command_doc="""
                Usage:
                    mk <summary> [CONTENT]
                """,
            parse_input=input_parser,
            present_output=output_presentor,
        ),
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
