import sys
import typing as t

from cli import ioc  # type: ignore
from cli.generator.docopt_generator import DocOptChain
from cli.presentors.note_presentor import present_note
from domain.use_cases import create_note


def output_presentor(output: create_note.Output):
    if output.errors:
        for e in output.errors:
            print("ERROR:", e)

    else:
        print("create note with id:", output.id)
        note = output.note
        if note is None:
            raise NotImplementedError()
        present_note(note)


def input_parser(args: t.Dict[str, t.Any]) -> create_note.Input:
    summary = args["SUMMARY"]
    content = args["CONTENT"]
    if args["help"]:
        print(command_doc)
        sys.exit(0)

    if args['--interactive']:
        content = ""
        enter_times = 0

        summary = input("summary>")

        while enter_times < 3 or not content:
            line = input("content>")
            if line == "":
                if enter_times >= 3 and not content:
                    print("enter content please or quit with Ctrl+C")
                enter_times += 1
            else:
                enter_times = 0
                content += line + "\n"
    return create_note.Input("1", summary, content)


command_doc = """Usage:
    mk SUMMARY CONTENT
    mk --interactive
    mk help

Options:
    --interactive       input note interactive. In this mode you enter 
                        summary as first line, and next lines will become 
                        content. To end content, press Enter 3 times.   
"""

create_note_chain = DocOptChain(
    usecase=create_note.UseCase,
    dependencies=dict(gateway=ioc.create_note_gateway),
    name="mk",
    command_doc=command_doc,
    parse_input=input_parser,
    present_output=output_presentor,
)
