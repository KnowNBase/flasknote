import typing as t

from domain.errors import NotFoundError
from domain.models import Note, User
from domain.use_cases.create_note import IGateway


class Gateway(IGateway):
    def __init__(self, note_repo, user_repo):
        self.users = user_repo
        self.note_repo = note_repo

    def get_user(self, user_id: str) -> User:
        user = self.users.get_user(user_id)
        if user is None:
            raise NotFoundError("user", user_id)
        return user

    def save_note(self, note: Note) -> t.Tuple[Note, str]:
        return self.note_repo.save(note)
