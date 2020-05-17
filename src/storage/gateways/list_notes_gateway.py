import typing as t

from domain.errors import NotFoundError
from domain.models import Note, User
from domain.use_cases.list_notes import IGateway, Spec, PageSpec
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

    def load_notes(self, specs: t.List[Spec]) -> t.List[Note]:
        result_notes = self.note_repo.all_notes()
        for s in specs:
            if isinstance(s, PageSpec):
                page = s.page - 1
                offset = s.items_per_page * page
                limit = s.items_per_page * (page + 1)
                result_notes = result_notes[offset:limit]
        return result_notes
