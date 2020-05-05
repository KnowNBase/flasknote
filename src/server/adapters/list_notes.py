import typing as t
from dataclasses import asdict

from flask import request  # type: ignore

from domain.use_cases.list_notes import Input, UseCase, Output
from server.generator import FlaskAPIChain
from server.ioc import list_notes_gateway


def parse(_: t.Dict[str, t.Any]) -> Input:
    page = int(request.args.get("page", 1))
    return Input(user_id="1", page=page)


def present(output: Output) -> t.Dict[str, t.Any]:
    error_dicts = []
    for e in output.errors:
        error_dict = asdict(e)
        error_dict["description"] = str(e)
        error_dict["error_type"] = repr(e)
        error_dicts.append(error_dict)
    notes = output.notes
    return dict(notes=notes, errors=error_dicts)


list_notes_chain = FlaskAPIChain(
    usecase=UseCase,
    parse_input=parse,
    present_output=present,
    dependencies=dict(gateway=list_notes_gateway),
    url_path="/notes/",
    method="GET",
)
