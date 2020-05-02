from dataclasses import dataclass


@dataclass
class BaseError(Exception):
    pass

@dataclass
class StorageError(BaseError):
    pass

@dataclass
class NotFoundError(StorageError):
    type: str
    id: str
