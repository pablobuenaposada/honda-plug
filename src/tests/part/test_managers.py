import pytest
from model_bakery import baker

from part.constants import SOURCE_EPCDATA, SOURCE_HONDAPARTSNOW
from part.models import Part, Stock


@pytest.mark.django_db
class TestPartManager:
    def test_stocked_parts_first(self):
        part1 = baker.make(Part, reference="foooo-bar-ban", source=SOURCE_EPCDATA)
        part2 = baker.make(Part, reference="foooo-bar-ban2", source=SOURCE_EPCDATA)
        baker.make(Stock, part=part2, source=SOURCE_HONDAPARTSNOW, country="US")
        part3 = baker.make(Part, reference="foooo-bar-ban3", source=SOURCE_EPCDATA)

        assert list(Part.objects.all()) == [part1, part2, part3]
        assert list(Part.objects.stocked_parts_first())[0] == part2

    def test_stocked_parts_last(self):
        part1 = baker.make(Part, reference="foooo-bar-ban1", source=SOURCE_EPCDATA)
        part2 = baker.make(Part, reference="foooo-bar-ban2", source=SOURCE_EPCDATA)
        baker.make(Stock, part=part2, source=SOURCE_HONDAPARTSNOW, country="US")
        part3 = baker.make(Part, reference="foooo-bar-ban3", source=SOURCE_EPCDATA)

        assert list(Part.objects.all()) == [part1, part2, part3]
        assert list(Part.objects.stocked_parts_last())[-1] == part2
