import typing as t

from domain.errors import NotFoundError
from domain.models import Note, User
from domain.use_cases.create_note import IGateway
from storage.repositories.dict_note_repository import DictNoteRepository
from storage.repositories.dict_user_repository import DictUserRepository


class Gateway(IGateway):
    def __init__(self):
        self.users = DictUserRepository()
        self.note_repo = DictNoteRepository()

    def get_user(self, user_id: str) -> User:
        user = self.users.get_user(user_id)
        if user is None:
            raise NotFoundError("user", user_id)
        return user

    def save_note(self, note: Note) -> t.Tuple[Note, str]:
        return self.note_repo.save(note)
