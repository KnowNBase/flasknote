import json
import os.path as path
import typing as t

import utils.json as dsjson
from domain.errors import NotFoundError
from domain.models import FreeNote, Tag


class Repository:
    SPLITTER = "\nKNBSPLITTER\n"

    def __init__(self, filepath):
        self.__notes_file = filepath
        self._notes = {}
        if path.isfile(filepath):
            with open(filepath, encoding="utf8") as f:
                data = f.read()
                if data:
                    notes = json.loads(data)
                    for id_, note in notes.items():
                        self._notes[id_] = self.__parse_note(note)

    # def __del__(self):
    #     try:
    #         self.sync_to_file()
    #     except Exception as e:
    #         print("Notes not sync: ", e)

    def all_notes(self):
        return list(self._notes.values())

    def get(self, id: str) -> FreeNote:
        if not self._notes.get(id):
            raise NotFoundError(type="note", id=id)
        return self._notes[id]

    def save(self, note: FreeNote) -> t.Tuple[FreeNote, str]:
        id_ = self.__newid()
        self._notes[id_] = note
        self.sync_to_file()
        return note, id_

    def __newid(self) -> str:
        if not self._notes:
            return str(1)
        lastid = list(self._notes.keys())[-1]
        return str(int(lastid) + 1)

    @staticmethod
    def __parse_note(data: dict) -> FreeNote:
        tags = [Tag(**d) for d in data["tags"]]
        return FreeNote(summary=data["summary"], content=data["content"], tags=tags)

    def sync_to_file(self):
        with open(self.__notes_file, "w", encoding="utf8") as f:
            data = dsjson.dumps(self._notes, indent=2)
            f.write(data)
