from typing import List, Optional
import json
from dataclasses import dataclass

# from server.models import Note, Tag


class Database:
    def __init__(self, filepath):
        self.filepath = filepath

    def write(self, data: dict) -> None:
        exists = self.all()
        exists.append(data)
        print("save data", exists)
        with open(self.filepath, "w") as f:
            f.write(json.dumps(exists))

    def all(self) -> List[Note]:
        with open(self.filepath) as f:
            content = f.read()
            if not content.strip():
                return []
        result = json.loads(content)
        if result is None:
            return []
        result = [Note(**r) for r in result]
        return result

    def get(self, name: str) -> Optional[Note]:
        return None


class MemoryStore:
    def __init__(self):
        self.notes = []

    def write(self, data: dict) -> None:
        self.notes.append(data)
