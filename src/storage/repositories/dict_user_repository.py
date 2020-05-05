from domain.errors import NotFoundError
from domain.models import User


class DictUserRepository:
    def __init__(self):
        self.users = {}

    def get_user(self, user_id: str) -> User:
        try:
            return self.users[user_id]
        except KeyError:
            raise NotFoundError("user", user_id)
