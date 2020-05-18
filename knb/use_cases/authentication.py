from abc import ABCMeta
from dataclasses import dataclass

from knb.errors import BaseError
from knb.use_cases import AbstractUseCase


@dataclass
class Input:
    user_id: str
    password_hash: str


@dataclass
class Session:
    name: str


@dataclass
class Output:
    session: Session


class IGateway(metaclass=ABCMeta):
    pass


@dataclass(eq=False)
class UseCase(AbstractUseCase[Input, Output]):
    """
    Authenticate user in system and create for him a session
    """

    gateway: IGateway

    def _exec(self, input: Input) -> Output:
        pass

    def _error_response(self, error: BaseError) -> Output:
        pass
