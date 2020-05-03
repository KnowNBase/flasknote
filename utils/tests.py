from mimesis import Text

from domain.models import Note

t = Text()


def generate_note():
    return Note(t.title(), t.sentence())
