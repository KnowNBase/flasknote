import typing as t
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field

from knb.errors import BaseError
from knb.models import Note, Tag, User
from knb.use_cases import AbstractUseCase
from knb.use_cases import specs


@dataclass
class Input:
    user_id: str


@dataclass
class Output:
    groups: t.Dict[Tag, t.List[Note]]
    errors: t.List[BaseError] = field(default_factory=list)


class IGateway(metaclass=ABCMeta):
    @abstractmethod
    def get_user(self, user_id: str) -> User:
        pass

    @abstractmethod
    def load_notes(self, spec: specs.Spec) -> t.List[Note]:
        pass


@dataclass(eq=False)
class UseCase(AbstractUseCase[Input, Output]):
    gateway: IGateway

    def _exec(self, input: Input) -> Output:
        spec = specs.AuthorSpec(author_id=input.user_id)
        notes = self.gateway.load_notes(spec)
        grouped: t.Dict[Tag, t.List[Note]] = {}

        for note in notes:
            for t in note.tags:
                group = grouped.get(t, [])
                group.append(note)
                grouped[t] = group
        return Output(groups=grouped)

    def _error_response(self, error: BaseError) -> Output:
        return Output(groups={}, errors=[error])
