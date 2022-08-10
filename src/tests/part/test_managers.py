import pytest
from model_bakery import baker

from part.models import Part, Stock


@pytest.mark.django_db
class TestPartManager:
    def test_stocked_parts_first(self):
        part1 = baker.make(Part, reference="foo-bar-banana1")
        part2 = baker.make(Part, reference="foo-bar-banana2")
        baker.make(Stock, part=part2)
        part3 = baker.make(Part, reference="foo-bar-banana3")

        assert list(Part.objects.all()) == [part1, part2, part3]
        assert list(Part.objects.stocked_parts_first()) == [part2, part3, part1]

    def test_stocked_parts_last(self):
        part1 = baker.make(Part, reference="foo-bar-banana1")
        part2 = baker.make(Part, reference="foo-bar-banana2")
        baker.make(Stock, part=part2)
        part3 = baker.make(Part, reference="foo-bar-banana3")

        assert list(Part.objects.all()) == [part1, part2, part3]
        assert list(Part.objects.stocked_parts_last()) == [part1, part3, part2]
