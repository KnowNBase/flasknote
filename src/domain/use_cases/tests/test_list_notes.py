from unittest.mock import Mock

import pytest  # type: ignore

from domain.use_cases import list_notes
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

    response: list_notes.Output = uc(list_notes.Input("1", 1))

    gateway.load_notes.assert_called_with([list_notes.PageSpec(1, 100)])
    assert not response.errors
    assert response.notes


# noinspection PyUnresolvedReferences
def test_list_other_page(gateway):
    uc = list_notes.UseCase(gateway)

    response: list_notes.Output = uc(list_notes.Input("1", 2))

    gateway.load_notes.assert_called_with([list_notes.PageSpec(2, 100)])
    assert not response.errors
    assert response.notes