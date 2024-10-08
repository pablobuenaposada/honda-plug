import pytest
from django.core.cache import cache
from freezegun import freeze_time
from model_bakery import baker
from part.constants import (
    CACHE_KEY_PARTS_TO_SNEAK,
    SOURCE_EPCDATA,
    SOURCE_HONDAPARTSNOW,
)
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

    @pytest.mark.parametrize(
        "date, days, expected",
        (
            ("2022-01-01", 1, ["FOOOO-BAR-BAN1"]),
            ("2022-01-02", 1, ["FOOOO-BAR-BAN1"]),
            ("2022-01-04", 1, ["FOOOO-BAR-BAN2", "FOOOO-BAR-BAN1"]),
        ),
    )
    def test_not_updated_since(self, date, days, expected):
        """
        part1 always is going to be returned since doesn't have stock so it always matches the "not updated since"
        part2 is only going to be returned if is within the range where more than x days passed
        """
        baker.make(Part, reference="foooo-bar-ban1", source=SOURCE_EPCDATA)  # part1
        part2 = baker.make(Part, reference="foooo-bar-ban2", source=SOURCE_EPCDATA)

        with freeze_time("2022-01-01"):
            baker.make(Stock, part=part2, source=SOURCE_HONDAPARTSNOW, country="US")
        with freeze_time("2022-01-02"):
            baker.make(Stock, part=part2, source=SOURCE_HONDAPARTSNOW, country="ES")

        with freeze_time(date):
            assert (
                list(
                    Part.objects.not_updated_since(days).values_list(
                        "reference", flat=True
                    )
                )
                == expected
            )

    def test_parts_to_scrap(self):
        part3 = baker.make(
            Part,
            reference="foooo-bar-ban3",
            source=SOURCE_EPCDATA,
            last_time_delivered="2022-12-30 10:00:00",
        )
        part4 = baker.make(
            Part,
            reference="foooo-bar-ban4",
            source=SOURCE_EPCDATA,
            last_time_delivered="2022-12-30 10:00:00",
        )
        part2 = baker.make(
            Part,
            reference="foooo-bar-ban2",
            source=SOURCE_EPCDATA,
            last_time_delivered="2022-12-01 10:00:00",
        )
        part1 = baker.make(Part, reference="foooo-bar-ban1", source=SOURCE_EPCDATA)

        assert list(Part.objects.parts_to_scrap()) == [part1, part2, part3, part4]

    def test_parts_to_scrap_with_sneak_parts(self):
        part1 = baker.make(Part, reference="foooo-bar-ban1", source=SOURCE_EPCDATA)
        part2 = baker.make(Part, reference="foooo-bar-ban2", source=SOURCE_EPCDATA)
        part3 = baker.make(Part, reference="foooo-bar-ban3", source=SOURCE_EPCDATA)
        cache.set(CACHE_KEY_PARTS_TO_SNEAK, [part1.reference, part2.reference])

        assert list(Part.objects.parts_to_scrap()) == [part1]
        assert cache.get(CACHE_KEY_PARTS_TO_SNEAK) == [part2.reference]
        assert list(Part.objects.parts_to_scrap()) == [part2]
        assert cache.get(CACHE_KEY_PARTS_TO_SNEAK) == []
        assert list(Part.objects.parts_to_scrap()) == [part1, part2, part3]
