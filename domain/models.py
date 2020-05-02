from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class Tag:
    """
    Just a label that marks some data with keywork.        
    """

    name: str


@dataclass
class Note:
    """
    short note. little knowledge. can has tags for 
    aggregation, search
    """

    summary: str
    description: str
    tags: List[Tag] = field(default_factory=list)


@dataclass
class Catalog:
    """
    Contains notes grouped by some condition: tag, manual,
    etc.
    """

    name: str
    notes: List[Note] = field(default_factory=list)
    tags: List[Tag] = field(default_factory=list)
