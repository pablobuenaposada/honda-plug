from unittest.mock import patch

import pytest
from djmoney.money import Money as DjangoMoney
from model_bakery import baker
from money import Money

from part.constants import SOURCE_AMAYAMA, SOURCE_EPCDATA, SOURCE_TEGIWA
from part.lambdas import add_stock
from part.models import Image, Part, Stock
from scrapper.common.stock import Stock as ParsedStock
from tests.utils import assert_part_main_fields, assert_stock_main_fields


@pytest.mark.django_db
@patch("part.tasks.search_for_stocks")
class TestLambdas:
    reference = "56483-PND-003"
    url = "http://foo.com"
    title = "foo"
    country = "US"
    available = True
    discontinued = False
    source = SOURCE_TEGIWA
    stock = ParsedStock(
        reference=reference,
        source=source,
        title=title,
        available=available,
        discontinued=discontinued,
        url=url,
        country=country,
        price=Money(currency="USD"),
    )
    expected_part = {
        "reference": reference,
        "source": source,
    }
    expected_stock = {
        "reference": reference,
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
        baker.make(Part, reference=self.reference, source=self.source)

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
        part = baker.make(Part, reference=self.reference, source=self.source)
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
