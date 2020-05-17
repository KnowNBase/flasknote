import pytest  # type: ignore

from server.ioc import list_notes_gateway
from server.server import app


@pytest.fixture
def flask_client():
    app.config["TESTING"] = True
    client = app.test_client()
    return client


def test_create_note(flask_client):
    flask_client.post("/notes/", json=dict(summary="title", content="text"))
    # TODO: use mock or test api or public api
    notes = list_notes_gateway.notes._notes
    assert len(notes) == 1
    assert notes["1"].summary == "title"
    assert notes["1"].content == "text"
    assert notes["1"].author


def test_get_notes(flask_client):
    flask_client.post("/notes/", json=dict(summary="title", content="text"))
    res = flask_client.get("/notes/")
    json = res.get_json()
    assert json["notes"]
    first_note = json["notes"][0]
    assert first_note["summary"] == "title", first_note
    assert first_note["content"] == "text", first_note
    assert first_note["tags"] == []
