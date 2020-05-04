import typing as t

from cli.generator.docopt_generator import DocOptChain
from domain.use_cases import list_notes
from storage.gateways import list_notes_gateway


def output_presentor(output: list_notes.Output):
    if output.errors:
        for e in output.errors:
            print("ERROR:", e)
    else:
        for note in output.notes:
            print(note.summary)
            if note.tags:
                print(f"{note.tags}")
            print("\t" + note.content)


def input_parser(args: t.Dict[str, t.Any]) -> list_notes.Input:
    pg = args["PAGE"]
    if not pg:
        pg = 1

    return list_notes.Input("1", pg)


list_notes_chain = DocOptChain(
    usecase=list_notes.UseCase,
    dependencies=dict(gateway=list_notes_gateway.Gateway()),
    name="list",
    command_doc="""
                List 
                Usage:
                    list [PAGE]
                """,
    parse_input=input_parser,
    present_output=output_presentor,
)
