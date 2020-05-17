import typing as t

from cli import ioc
from cli.generator.docopt_generator import DocOptChain
from domain.use_cases import create_note


def output_presentor(output: create_note.Output):
    if output.errors:
        for e in output.errors:
            print("ERROR:", e)
    else:
        print(f"note '{output.note}' created")


def input_parser(args: t.Dict[str, t.Any]) -> create_note.Input:
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
    return create_note.Input("1", summary, content)


create_note_chain = DocOptChain(
    usecase=create_note.UseCase,
    dependencies=dict(gateway=ioc.create_note_gateway),
    name="mk",
    command_doc="""
                Usage:
                    mk <summary> [CONTENT]
                """,
    parse_input=input_parser,
    present_output=output_presentor,
)
