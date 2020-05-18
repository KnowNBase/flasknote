from abc import ABCMeta
from dataclasses import dataclass

from knb.errors import BaseError
from knb.use_cases import AbstractUseCase


@dataclass
class Input:
    pass


@dataclass
class Output:
    pass


class IGateway(metaclass=ABCMeta):
    pass


@dataclass(eq=False)
class UseCase(AbstractUseCase[Input, Output]):
    gateway: IGateway

    def _exec(self, input: Input) -> Output:
        pass

    def _error_response(self, error: BaseError) -> Output:
        pass
