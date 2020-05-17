from domain.models import Note


def present_note(note: Note):
    print(note.summary)
    print("-" * len(note.summary))
    if note.tags:
        tags_str = ", ".join(["#" + tag.name for tag in note.tags])
        print(tags_str)
    maxline = max([len(l) for l in note.content.splitlines()])
    print("*" * maxline)
    print(note.content)
    print("*" * maxline)
