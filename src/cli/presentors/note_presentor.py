from domain.models import Note


def present_note(note: Note):
    print(note.summary)
    print()
    if note.tags:
        tags_str = ",".join([f"[{tag.name}]" for tag in note.tags])
        print(tags_str)
    print(note.content)
