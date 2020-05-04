import typing as t
from dataclasses import dataclass


@dataclass
class Chain:
    usecase: t.Type
    dependencies: t.Dict[str, t.Any]
    parse_input: t.Callable[[t.Dict[str, t.Any]], t.Any]
    present_output: t.Callable

    def compose(self) -> t.Callable[[t.Dict[str, t.Any]], t.Any]:
        def use_case_function(args):
            UseCase = self.usecase
            uc = UseCase(**self.dependencies)
            input_ = self.parse_input(args)
            output = uc(input_)
            return self.present_output(output)

        return use_case_function
