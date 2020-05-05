from domain.use_cases.list_notes import PageSpec
from storage.gateways.list_notes_gateway import Gateway
from utils.tests import generate_note


def test_list_page1():
    gw = Gateway()
    gw.note_repo._notes = {str(i): generate_note() for i in range(0, 150)}
    spec = PageSpec(1, 100)

    notes = gw.load_notes([spec])

    assert len(notes) == 100

    spec = PageSpec(2, 100)

    notes = gw.load_notes([spec])

    assert len(notes) == 50
