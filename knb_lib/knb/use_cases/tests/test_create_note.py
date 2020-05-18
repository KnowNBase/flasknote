from unittest.mock import Mock

import pytest  # type: ignore

from knb.use_cases import create_note
from knb.utils import factory


def test_creation():
    note = factory.create_note()
    gateway: create_note.IGateway = Mock()
    gateway.save_note.return_value = (
        note,
        "1",
    )
    gateway.get_user.return_value = note.author
    uc = create_note.UseCase(gateway)
    request = create_note.Input(user_id="1", summary=note.summary, content=note.content)
    response = uc(request)

    # noinspection PyUnresolvedReferences
    gateway.get_user.assert_called_with("1")
    # noinspection PyUnresolvedReferences
    gateway.save_note.assert_called_with(note)

    assert not response.errors
    # check that UC returs results of gateway
    assert response.id == "1"
    assert response.note == note


def test_gataway_dead():
    gateway: create_note.IGateway = Mock()
    gateway.get_user.side_effect = Exception("service not available")
    uc = create_note.UseCase(gateway)
    # bypass unknown exceptions
    with pytest.raises(Exception):
        out: create_note.Output = uc(
            create_note.Input("1", "unnamed", "mock can save me")
        )
