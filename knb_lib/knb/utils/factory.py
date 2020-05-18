import typing as t

import mimesis  # type: ignore

from knb.models import User, Note, Tag

person = mimesis.Person()
text = mimesis.Text()


def create_user():
    return User(
        username=person.username(),
        first_name=person.first_name(),
        last_name=person.last_name(),
        middle_name=person.surname(),
    )


def create_note(tags: t.List[Tag] = None) -> Note:
    if tags is None:
        tags = []
    return Note(
        summary=text.title(),
        content=text.text(),
        tags=tags,
        author=create_user()
    )
