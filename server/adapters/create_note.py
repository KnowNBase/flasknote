import typing as t
from dataclasses import asdict

from flask import request  # type: ignore

from knb.use_cases import UseCase, Input, Output
from server.generator import FlaskAPIChain
from server.ioc import create_note_gateway


def input_parser(_: t.Dict[str, t.Any]) -> Input:
    # errors = validate(Note, request.get_json())
    # TODO: optional fields or fields from other data stores, like auth session
    summary = request.get_json().get("summary", "")  # type: ignore
    content = request.get_json().get("content", "")  # type: ignore
    return Input(user_id="1", summary=summary, content=content)


def output_presentor(output: Output) -> dict:
    return asdict(output)


create_note_chain = FlaskAPIChain(
    usecase=UseCase,
    dependencies=dict(gateway=create_note_gateway),
    parse_input=input_parser,
    present_output=output_presentor,
    method="POST",
    url_path="/notes/",
)