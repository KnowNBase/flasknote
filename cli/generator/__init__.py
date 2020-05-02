import typing as t
from dataclasses import dataclass


@dataclass
class Chain:
    usecase: t.Type
    dependencies: t.Dict[str, t.Any]
    command_doc: str
    command_name: str
    parse_input: t.Callable[[t.Dict[str, t.Any]], t.Any]
    present_output: t.Callable
