import typing as t
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field

from knb.errors import BaseError
from knb.models import Note, Tag, User
from knb.use_cases import AbstractUseCase


class IGateway(metaclass=ABCMeta):
    @abstractmethod
    def get_user(self, user_id: str) -> User:
        pass

    @abstractmethod
    def save_note(self, note: Note) -> t.Tuple[Note, str]:
        pass


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


@dataclass(eq=False)
class UseCase(AbstractUseCase[Input, Output]):
    gateway: IGateway

    def _exec(self, input: Input) -> Output:
        # found = SearchNoteService.find_fuzzy(summary, content)
        # if found:
        #     return found[0]
        # else:
        user = self.gateway.get_user(input.user_id)
        tags = [Tag(name=n) for n in input.tags]
        note = Note(
            summary=input.summary, content=input.content, tags=tags, author=user
        )
        saved, id_ = self.gateway.save_note(note)
        return Output(note=saved, id=id_)

    def _error_response(self, error: BaseError) -> Output:
        return Output(errors=[error])
