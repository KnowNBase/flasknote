import typing as t
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field

from knb.errors import BaseError
from knb.models import User, Note
from knb.use_cases import AbstractUseCase
from knb.use_cases import specs


class IGateway(metaclass=ABCMeta):
    @abstractmethod
    def get_user(self, user_id: str) -> User:
        pass

    @abstractmethod
    def load_notes(self, specs: t.List[specs.Spec]) -> t.List[Note]:
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
        spec: specs.Spec = specs.AuthorSpec(input.user_id)
        spec = spec.and_spec(specs.PageSpec(input.page, 100))
        notes = self.gateway.load_notes([spec])
        return Output(notes=notes)

    def _error_response(self, error: BaseError) -> Output:
        return Output(errors=[error])

    # class Meta:
    #     require_permissions = Permission.ViewNotes
