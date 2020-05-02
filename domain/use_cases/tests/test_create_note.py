from unittest.mock import Mock

from domain.errors import StorageError
from domain.models import Note
from domain.use_cases.create_note import CreateNote, ICreateNoteGateway


# noinspection PyUnresolvedReferences
def test_creation():
    gateway: ICreateNoteGateway = Mock()
    gateway.save_note.return_value = (
        Note("TDD", "Tests first, but i make it little bit later", []),
        "noteid",
    )
    uc = CreateNote(gateway)
    request = CreateNote.Input(
        "1", "TDD", "Tests first, but i make it little bit later"
    )
    response = uc(request)

    gateway.get_user.assert_called_with("1")
    gateway.save_note.assert_called_with(
        Note("TDD", "Tests first, but i make it little bit later", [])
    )

    assert not response.errors
    # check that UC returs results of gateway
    assert response.id == "noteid"
    assert response.note == Note(
        "TDD", "Tests first, but i make it little bit later", []
    )


def test_gataway_dead():
    gateway: ICreateNoteGateway = Mock()
    gateway.get_user.side_effect = Exception("service not available")
    uc = CreateNote(gateway)
    out = uc.Output = uc(uc.Input("1", "unnamed", "mock can save me"))
    assert out.errors
    assert StorageError() in out.errors
