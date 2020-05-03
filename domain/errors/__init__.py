from dataclasses import dataclass


@dataclass
class BaseError(Exception):
    def __str__(self):
        return "Unknown error"


@dataclass
class StorageError(BaseError):
    def __str__(self):
        return "Storage error"


@dataclass
class NotFoundError(StorageError):
    type: str
    id: str

    def __str__(self):
        return f"Not found {self.type} with id {self.id}"
