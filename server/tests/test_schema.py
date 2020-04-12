from server.schema import validate, NotFoundKeyError, WrongTypeError
import pytest
from dataclasses import dataclass
# what about check real data?
from server.database import Note

# Our example data We can declare them in fixtures, but i 
# don't like move out some "private" data for this tests
# Look at them. We expect, that we good understand this
# structure, so we understand errors and payload

@dataclass
class Payload:
    data: int


@dataclass
class Under:
    v: Payload


@dataclass
class Nested:
    data: Payload
    un: Under

# as like "json-schema", we can declare them like this:
# {
#   "data": {
#     "data": int
#   },
#   "un": {
#     "v": {
#       "data": int
#     }
#   }
# }

def test_errors_eq():
    """
    Just for confirm, that we can check test, like 
    ``NotFoundKeyError("data") in errors`` without parsing
    error object
    """
    assert NotFoundKeyError("a") == NotFoundKeyError("a")
    assert NotFoundKeyError("B") != NotFoundKeyError("b")

    assert WrongTypeError("a", int, str) == WrongTypeError("a", int, str)
    assert WrongTypeError("a", int, str) != WrongTypeError("a", int, int)
    assert WrongTypeError("a", int, str) != WrongTypeError("a", str, str)


def test_simple_data():
    errors = validate(Payload, dict())
    assert NotFoundKeyError("data") in errors

    errors = validate(Payload, dict(data="s"))
    assert WrongTypeError("data", int, str) in errors


def test_nesting():
    assert not validate(Nested, {
        "data": { "data": 5 },
        "un": { "v": { "data": 5 } }
    })
    
    errors = validate(Nested, {
        "data": { "data": "v" },
        "un": { "v": { "data": 5 } }
    })
    assert WrongTypeError("data.data", int, str) in errors
    
    errors = validate(Nested, {
        "data": { "data": 5 },
        "un": { "v": { "data": "5" } }
    })
    assert WrongTypeError("un.v.data", int, str) in errors


def test_multiple_errors():
    errors = validate(Nested, dict())
    assert len(errors) == 2
    assert NotFoundKeyError("un") in errors
    assert NotFoundKeyError("data") in errors

    errors = validate(Nested, {
        "data": { "data": True },
        "un": { "v": { "data": "wrong" } }
    })
    assert len(errors) == 2
    assert WrongTypeError("un.v.data", int, str) in errors
    assert WrongTypeError("data.data", int, bool) in errors


def test_real_data():
    errors = validate(Note, {
        "summary": "name",
        "description": "long text",
        "tags": []
    })
    assert not errors
    
    errors = validate(Note, {
        "summary": "name",
        "description": "long text",
        "tags": [ { "bullshit": True } ]
    })
    assert errors
    assert NotFoundKeyError("tags.[0].name") in errors