from abc import ABCMeta, abstractmethod
from functools import wraps

from domain.models import Note, Tag, User
import typing as t
from dataclasses import dataclass, field

from domain.errors import BaseError, StorageError, NotFoundError


class ICreateNoteGateway(metaclass=ABCMeta):
    @abstractmethod
    def get_user(self, user_id: str) -> User:
        pass

    @abstractmethod
    def save_note(self, note: Note) -> t.Tuple[Note, str]:
        pass


@dataclass(eq=False)
class CreateNote:
    gateway: ICreateNoteGateway

    @dataclass
    class Input:
        user_id: str
        summary: str
        content: str
        tags: t.List[str] = field(default_factory=list)

    @dataclass
    class Output:
        note: t.Optional[Note] = None
        id: t.Optional[str] = None
        errors: t.List[BaseError] = field(default_factory=list)

    def exec(self, input_: "Input") -> "Output":
        # found = SearchNoteService.find_fuzzy(summary, content)
        # if found:
        #     return found[0]
        # else:
        try:
            user = self.gateway.get_user(input_.user_id)
        except NotFoundError as e:
            return self.__error_response(e)
        except Exception:
            output = self.__error_response(StorageError())
            return output

        tags = [Tag(name=n) for n in input_.tags]
        note = Note(summary=input_.summary, content=input_.content, tags=tags)
        try:
            saved, id_ = self.gateway.save_note(note)
        except Exception:
            output = self.__error_response(StorageError())
            return output

        return self.Output(note=saved, id=id_)

    def __error_response(self, error: BaseError) -> "Output":
        return self.Output(errors=[error])
