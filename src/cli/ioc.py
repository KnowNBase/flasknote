import os


def __init():
    from domain.models import User
    from storage.repositories.users import dict_memory
    from storage.gateways import list_notes_gateway as list_notes
    from storage.gateways import create_note_gateway as create_note
    from storage.repositories.notes import json_file

    users_repo = dict_memory.Repository()
    users_repo.users["1"] = User("admin", "first", "last", "middle")

    notes_repo = json_file.Repository(os.path.curdir + "/notes.knb")

    list_notes_gateway = list_notes.Gateway(notes_repo, users_repo)
    create_note_gateway = create_note.Gateway(notes_repo, users_repo)

    return list_notes_gateway, create_note_gateway


list_notes_gateway, create_note_gateway = __init()
