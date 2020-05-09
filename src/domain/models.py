import typing as t
from dataclasses import dataclass, field


@dataclass
class Tag:
    """
    Just a label that marks some data with keywork.        
    """

    name: str


@dataclass
class User:
    """
    So, it's user
    """
    username: str
    first_name: str
    last_name: str
    middle_name: str


@dataclass
class Note:
    """
    short note. little knowledge. can has tags for 
    aggregation, search
    """

    summary: str
    content: str
    author: User
    tags: t.List[Tag] = field(default_factory=list)


@dataclass
class Catalog:
    """
    Contains notes grouped by some condition: tag, manual,
    etc.
    """

    name: str
    notes: t.List[Note] = field(default_factory=list)
    tags: t.List[Tag] = field(default_factory=list)
