import os


def __init():
    from domain.models import User
    from storage.repositories.dict_user_repository import DictUserRepository
    from storage.gateways import list_notes_gateway as list_notes
    from storage.gateways import create_note_gateway as create_note
    from storage.repositories import file_note

    users_repo = DictUserRepository()
    users_repo.users["1"] = User("admin", "first", "last", "middle")

    notes_repo = file_note.Repository(os.path.curdir + "/notes.knb")

    list_notes_gateway = list_notes.Gateway()
    list_notes_gateway.users = users_repo
    list_notes_gateway.note_repo = notes_repo

    create_note_gateway = create_note.Gateway()
    create_note_gateway.users = users_repo
    create_note_gateway.note_repo = notes_repo

    return list_notes_gateway, create_note_gateway


list_notes_gateway, create_note_gateway = __init()
