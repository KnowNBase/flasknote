import mimesis  # type: ignore

from domain.models import User


def create_user():
    p = mimesis.Person()
    return User(
        username=p.username(),
        first_name=p.first_name(),
        last_name=p.last_name(),
        middle_name=p.surname()
    )
