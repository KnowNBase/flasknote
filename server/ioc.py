def __init():
    from knb.models import User
    import storage.repositories.users.dict_memory as users_memory
    import storage.repositories.notes.dict_memory as notes_memory
    from storage.gateways import list_notes_gateway as list_notes
    from storage.gateways import create_note_gateway as create_note

    users_repo = users_memory.Repository()
    users_repo.users["1"] = User("admin", "first", "last", "middle")
    notes_repo = notes_memory.Repository()
    list_notes_gateway = list_notes.Gateway(notes_repo, users_repo)
    create_note_gateway = create_note.Gateway(notes_repo, users_repo)

    return list_notes_gateway, create_note_gateway


list_notes_gateway, create_note_gateway = __init()
