from unittest.mock import patch

import pytest
from djmoney.money import Money as DjangoMoney
from model_bakery import baker
from money import Money
from part.constants import SOURCE_TEGIWA, SOURCE_UNKNOWN
from part.lambdas import add_part, add_stock
from part.models import Image, Part, Stock
from scrapper.common.stock import Stock as ParsedStock
from tests.utils import assert_part_main_fields, assert_stock_main_fields

REFERENCE = "56483-PND-003"


@pytest.mark.django_db
@patch("part.models.search_for_stocks")
class TestAddStock:
    url = "http://foo.com"
    title = "foo"
    country = "US"
    available = True
    discontinued = False
    source = SOURCE_TEGIWA
    stock = ParsedStock(
        reference=REFERENCE,
        source=source,
        title=title,
        available=available,
        discontinued=discontinued,
        url=url,
        country=country,
        price=Money(currency="USD"),
    )
    expected_part = {
        "reference": REFERENCE,
        "source": source,
        "last_time_delivered": None,
    }
    expected_stock = {
        "reference": REFERENCE,
        "country": country,
        "url": url,
        "title": title,
        "source": source,
        "price": DjangoMoney(0, "USD"),
        "available": available,
        "discontinued": discontinued,
        "quantity": None,
    }

    def test_add_stock_empty_db(self, m_search_for_stocks):
        assert Part.objects.count() == 0
        assert Stock.objects.count() == 0
        assert Image.objects.count() == 0

        add_stock(self.stock)

        assert Part.objects.count() == 1
        assert Stock.objects.count() == 1
        assert Image.objects.count() == 0

        assert_part_main_fields(Part.objects.first(), self.expected_part)
        assert_stock_main_fields(Stock.objects.first(), self.expected_stock)

    def test_add_stock_part_found(self, m_search_for_stocks):
        baker.make(Part, reference=REFERENCE, source=self.source)

        assert Part.objects.count() == 1
        assert Stock.objects.count() == 0
        assert Image.objects.count() == 0

        add_stock(self.stock)

        assert Part.objects.count() == 1
        assert Stock.objects.count() == 1
        assert Image.objects.count() == 0

        assert_part_main_fields(Part.objects.first(), self.expected_part)
        assert_stock_main_fields(Stock.objects.first(), self.expected_stock)

    def test_add_stock_part_found_and_stock_found(self, m_search_for_stocks):
        part = baker.make(Part, reference=REFERENCE, source=self.source)
        baker.make(Stock, part=part, source=self.source, country=self.country)

        assert Part.objects.count() == 1
        assert Stock.objects.count() == 1
        assert Image.objects.count() == 0

        add_stock(self.stock)

        assert Part.objects.count() == 1
        assert Stock.objects.count() == 1
        assert Image.objects.count() == 0

        assert_part_main_fields(Part.objects.first(), self.expected_part)
        assert_stock_main_fields(Stock.objects.first(), self.expected_stock)


@pytest.mark.django_db
@patch("part.models.search_for_stocks")
class TestAddPart:
    source = SOURCE_UNKNOWN

    def test_part_not_found(self, m_search_for_stocks):
        assert Part.objects.count() == 0
        assert type(add_part(REFERENCE, self.source)) == Part
        assert Part.objects.count() == 1

    @pytest.mark.parametrize(
        "reference, reference_to_search, expected_num_parts",
        (
            (REFERENCE, REFERENCE, 1),
            (REFERENCE, REFERENCE.lower(), 1),
            (REFERENCE, REFERENCE.upper(), 1),
            (REFERENCE, REFERENCE.replace("-", ""), 1),
            ("89000-SM4-000ZA", "89000-SM4-000", 2),
        ),
    )
    def test_part_found(
        self, m_search_for_stocks, reference, reference_to_search, expected_num_parts
    ):
        baker.make(Part, reference=reference, source=self.source)

        assert Part.objects.count() == 1
        assert type(add_part(reference_to_search, self.source)) == Part
        assert Part.objects.count() == expected_num_parts
