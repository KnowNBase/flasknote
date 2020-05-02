from unittest.mock import Mock

from cli.docopt_generator import Generator
from cli.generator import Chain
from domain.models import Note
from domain.use_cases.create_note import CreateNote, ICreateNoteGateway


# noinspection PyUnresolvedReferences
def test_create_one_command():
    note = Note("note title", "note content")
    gw: ICreateNoteGateway = Mock()
    input_parser = Mock()
    input_parser.return_value = CreateNote.Input("1", note.summary, note.content)
    output_presentor = Mock()
    links = [
        Chain(
            usecase=CreateNote,
            dependencies=dict(gateway=gw),
            command_name="mk",
            command_doc="""
            Usage:
                mk <summary> [CONTENT]
            """,
            parse_input=input_parser,
            present_output=output_presentor,
        )
    ]
    g = Generator()
    commands = g(links)
    assert commands
    create_note = commands["mk"]
    create_note(["mk", note.summary, note.content])
    gw.save_note.assert_called_with(note)
