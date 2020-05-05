from dataclasses import dataclass


@dataclass(repr=False)
class BaseError(Exception):
    def __str__(self):
        return "Unknown error"

    def __repr__(self):
        return self.__class__.__name__


@dataclass(repr=False)
class StorageError(BaseError):
    def __str__(self):
        return "Storage error"


@dataclass(repr=False)
class NotFoundError(StorageError):
    type: str
    id: str

    def __str__(self):
        return f"Not found {self.type} with id {self.id}"


@dataclass(repr=False)
class CommonError(BaseError):
    message: str
