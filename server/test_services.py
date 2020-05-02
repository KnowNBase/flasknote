from mimesis import Text
from domain.models import Note, Tag, Catalog
from unittest import mock
from services import CatalogService


def test_tag_aggregation():
    tg = Text()
    notes = [
        Note(tg.title(), tg.text(), [Tag("One", Tag("Two"))]),
        Note(tg.title(), tg.text(), [Tag("One", Tag("Two"))]),
        Note(tg.title(), tg.text(), [Tag("One")]),
    ]

    service = CatalogService()
    catalogs = service.create_catalogs_by_tag(notes)
    # storage = mock.Mock()
    # storage.save(catalogs)
    assert len(catalogs) == 2
    assert Tag("One") in catalogs[0].tags
    assert Tag("Two") in catalogs[0].tags
    assert Tag("One") in catalogs[1].tags
    assert Tag("Two") not in catalogs[1].tags
