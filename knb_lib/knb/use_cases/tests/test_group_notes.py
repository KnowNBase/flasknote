from unittest.mock import Mock

from knb.models import Tag
from knb.use_cases import group_by_tag
from knb.utils import factory


def test_grouping():
    tag_one = Tag("one")
    tag_two = Tag("two")

    gateway: group_by_tag.IGateway = Mock()
    notes = [factory.create_note(tags=[tag_one]) for _ in range(3)]
    notes.extend([factory.create_note(tags=[tag_two]) for _ in range(5)])
    gateway.load_notes.return_value = notes

    input = group_by_tag.Input(user_id="1")

    uc = group_by_tag.UseCase(gateway)
    result: group_by_tag.Output = uc(input)
    groups = result.groups
    assert len(groups.keys()) == 2
    assert len(groups[tag_one]) == 3
    assert len(groups[tag_two]) == 5


def test_overlap_grouping():
    tag_one = Tag("one")
    tag_two = Tag("two")

    gateway: group_by_tag.IGateway = Mock()
    note1 = factory.create_note(tags=[tag_one, tag_two])
    note2 = factory.create_note(tags=[tag_two])
    notes = [
        note1,
        note2,
    ]

    gateway.load_notes.return_value = notes

    input = group_by_tag.Input(user_id="1")

    uc = group_by_tag.UseCase(gateway)
    result: group_by_tag.Output = uc(input)
    groups = result.groups
    assert len(groups.keys()) == 2
    assert len(groups[tag_one]) == 1
    assert len(groups[tag_two]) == 2
    assert note1 in groups[tag_two] and note1 in groups[tag_one]
    assert note2 in groups[tag_two] and not note2 in groups[tag_one]
