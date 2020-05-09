from unittest.mock import Mock

import pytest  # type: ignore

from domain.use_cases import list_notes
from domain.use_cases.list_notes import AuthorSpec, PageSpec
from utils.tests import generate_note


# noinspection Mypy


@pytest.fixture
def gateway() -> list_notes.IGateway:
    mock = Mock()
    mock.load_notes.return_value = [generate_note() for i in range(150)]
    return mock


# noinspection PyUnresolvedReferences
def test_list_notes(gateway):
    uc = list_notes.UseCase(gateway)

    response: list_notes.Output = uc(list_notes.Input(user_id="1", page=1))
    spec = list_notes.AuthorSpec("1").and_spec(list_notes.PageSpec(1, 100))
    gateway.load_notes.assert_called_with([spec])
    assert not response.errors
    assert response.notes


# noinspection PyUnresolvedReferences
def test_list_other_page(gateway):
    uc = list_notes.UseCase(gateway)

    response: list_notes.Output = uc(list_notes.Input(user_id="1", page=2))
    spec = list_notes.AuthorSpec("1").and_spec(list_notes.PageSpec(2, 100))
    gateway.load_notes.assert_called_with([spec])
    assert not response.errors
    assert response.notes


def test_list_my_notes(gateway):
    uc = list_notes.UseCase(gateway)
    input = list_notes.Input("1", 1)
    result: list_notes.Output = uc(input)
    author_spec = AuthorSpec("1")
    page_spec = PageSpec(1, 100)
    spec = author_spec.and_spec(page_spec)
    # noinspection PyUnresolvedReferences
    gateway.load_notes.assert_called_with([spec])
