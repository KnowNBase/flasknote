from domain.models import Note
from domain.errors import NotFoundError
import typing as t


class DictNoteRepository:
    def __init__(self):
        self.notes = {}

    def get(self, id: str) -> Note:
        if not self.notes.get(id):
            raise NotFoundError(type="note", id=id)
        return self.notes[id]

    def save(self, note: Note) -> t.Tuple[Note, str]:
        id_ = self.__newid()
        self.notes[id_] = note
        return note, id_

    def __newid(self) -> str:
        if not self.notes:
            return str(1)
        lastid = list(self.notes.keys())[-1]
        return str(int(lastid) + 1)
