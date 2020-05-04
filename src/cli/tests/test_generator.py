from unittest.mock import Mock

from cli.generator.docopt_generator import Generator, DocOptChain
from domain.models import Note
from domain.use_cases import create_note


# noinspection PyUnresolvedReferences
def test_create_one_command():
    note = Note("note title", "note content")
    gw: IGateway = Mock()
    input_parser = Mock()
    input_parser.return_value = create_note.Input("1", note.summary, note.content)
    output_presentor = Mock()
    chains = [
        DocOptChain(
            usecase=create_note.UseCase,
            dependencies=dict(gateway=gw),
            name="mk",
            command_doc="""
            Usage:
                mk <summary> [CONTENT]
            """,
            parse_input=input_parser,
            present_output=output_presentor,
        )
    ]
    g = Generator()
    commands = g(chains)
    assert commands
    create_note_cmd = commands["mk"]
    create_note_cmd([note.summary, note.content])
    gw.save_note.assert_called_with(note)
