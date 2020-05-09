import typing as t
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field

from domain.errors import BaseError
from domain.models import User, Note
from domain.use_cases import AbstractUseCase


class Spec:
    def and_spec(self, other: "Spec") -> "Spec":
        return AndSpec(self, other)

    def or_spec(self, other: "Spec") -> "Spec":
        return OrSpec(self, other)


@dataclass
class OrSpec(Spec):
    left: Spec
    right: Spec


@dataclass
class AndSpec(Spec):
    left: Spec
    right: Spec


@dataclass
class PageSpec(Spec):
    page: int
    items_per_page: int


@dataclass
class AuthorSpec(Spec):
    author_id: str


class IGateway(metaclass=ABCMeta):
    @abstractmethod
    def get_user(self, user_id: str) -> User:
        pass

    @abstractmethod
    def load_notes(self, specs: t.List[Spec]) -> t.List[Note]:
        pass


@dataclass
class Input:
    user_id: str
    page: int


@dataclass
class Output:
    notes: t.List[Note] = field(default_factory=list)
    errors: t.List[BaseError] = field(default_factory=list)


@dataclass(eq=False)
class UseCase(AbstractUseCase[Input, Output]):
    gateway: IGateway

    def _exec(self, input: Input) -> Output:
        user = self.gateway.get_user(input.user_id)
        # check permission
        # self.permission_service.check_user(user, self)
        spec: Spec = AuthorSpec(input.user_id)
        spec = spec.and_spec(PageSpec(input.page, 100))
        notes = self.gateway.load_notes([spec])
        return Output(notes=notes)

    def _error_response(self, error: BaseError) -> Output:
        return Output(errors=[error])

    # class Meta:
    #     require_permissions = Permission.ViewNotes
