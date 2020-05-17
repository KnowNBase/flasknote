import tempfile

from domain.models import FreeNote, Tag
from storage.repositories.file_note import Repository


def test_note_create():
    _, storefile = tempfile.mkstemp()
    repo = Repository(storefile)

    assert len(repo.all_notes()) == 0

    note = FreeNote(
        summary="title", content="text", tags=[Tag(name="dumb"), Tag(name="data")]
    )
    repo.save(note)
    repo.sync_to_file()
    repo = Repository(storefile)

    assert len(repo.all_notes()) == 1
    assert repo.get("1") == note

    repo.sync_to_file()
    note2 = FreeNote(summary="another", content="eee", tags=[])
    repo = Repository(storefile)
    n, id_ = repo.save(note2)

    assert id_ == "2"

    repo.sync_to_file()
    repo = Repository(storefile)

    assert len(repo.all_notes()) == 2
    assert repo.get("1") == note
    assert repo.get("2") == note2
