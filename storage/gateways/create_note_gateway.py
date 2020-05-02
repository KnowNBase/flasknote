import typing as t

from domain.errors import NotFoundError
from domain.models import Note, User
from domain.use_cases.create_note import ICreateNoteGateway
from storage.repositories.dict_note_repository import DictNoteRepository


class DictCreateNoteGateway(ICreateNoteGateway):
    def __init__(self):
        self.users = {}
        self.note_repo = DictNoteRepository()

    def get_user(self, user_id: str) -> User:
        user = self.users.get(user_id)
        if user is None:
            raise NotFoundError("user", user_id)
        return user

    def save_note(self, note: Note) -> t.Tuple[Note, str]:
        return self.note_repo.save(note)
