import typing as t
from abc import abstractmethod, ABCMeta

from domain.errors import BaseError, StorageError

Output = t.TypeVar("Output")
Input = t.TypeVar("Input")


class AbstractUseCase(t.Generic[Input, Output], metaclass=ABCMeta):
    def __call__(self, input: Input) -> Output:
        try:
            return self._exec(input)
        except BaseError as e:
            return self._error_response(e)
        except Exception as e:
            return self._error_response(StorageError())

    @abstractmethod
    def _exec(self, input: Input) -> Output:
        pass

    @abstractmethod
    def _error_response(self, error: BaseError) -> Output:
        pass
