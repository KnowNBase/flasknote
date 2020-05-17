import typing as t
from abc import ABCMeta, abstractmethod

from domain.models import Note


class INotesRepository(metaclass=ABCMeta):
    @abstractmethod
    def all_notes(self) -> t.List[Note]:
        """

        """

    @abstractmethod
    def get(self, id: str) -> Note:
        """

        """

    @abstractmethod
    def save(self, note: Note) -> t.Tuple[Note, str]:
        """

        """
