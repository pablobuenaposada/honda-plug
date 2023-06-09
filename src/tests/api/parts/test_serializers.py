from unittest.mock import patch

import pytest
from api.parts.serializers import (
    HistoricalStockNestedOutputSerializer,
    PartOutputSerializer,
    StockNestedOutputSerializer,
    StockOutputSerializer,
)
from django.conf import settings
from django.utils.timezone import get_current_timezone
from djmoney.money import Money
from model_bakery import baker
from part.constants import SOURCE_TEGIWA
from part.models import Part, Stock

REFERENCE = "56483-PND-003"


@pytest.mark.django_db
@patch("part.models.search_for_stocks")
class TestsStockNestedOutputSerializer:
    serializer_class = StockNestedOutputSerializer

    def test_success(self, m_search_for_stocks):
        part = baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)
        stock = baker.make(Stock, part=part, source=SOURCE_TEGIWA, country="US")

        assert self.serializer_class(stock).data == {"id": stock.id}


@pytest.mark.django_db
@patch("part.models.search_for_stocks")
class TestsPartOutputSerializer:
    serializer_class = PartOutputSerializer

    def test_success(self, m_search_for_stocks):
        part = baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)

        assert self.serializer_class(part).data == {
            "reference": part.reference,
            "stock": [],
        }


@pytest.mark.django_db
@patch("part.models.search_for_stocks")
class TestsHistoricalStockNestedOutputSerializer:
    serializer_class = HistoricalStockNestedOutputSerializer

    def test_success(self, m_search_for_stocks):
        part = baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)
        stock = baker.make(
            Stock,
            part=part,
            source=SOURCE_TEGIWA,
            country="US",
            available=True,
            discontinued=True,
            price=Money(1, "USD"),
            _fill_optional=["quantity"],
        )

        assert self.serializer_class(stock).data == {
            "price": "{:,.2f}".format(stock.price.amount),
            "price_currency": stock.price_currency,
            "modified": stock.modified.astimezone(tz=get_current_timezone()).strftime(
                settings.REST_FRAMEWORK["DATETIME_FORMAT"]
            ),
        }


@pytest.mark.django_db
@patch("part.models.search_for_stocks")
class TestStockOutputSerializer:
    serializer_class = StockOutputSerializer

    def test_success(self, m_search_for_stocks):
        part = baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)
        stock = baker.make(
            Stock,
            part=part,
            source=SOURCE_TEGIWA,
            country="US",
            available=True,
            discontinued=True,
            price=Money(1, "USD"),
            _fill_optional=["quantity"],
        )
        stock.price = Money(2, "USD")
        stock.save()

        assert self.serializer_class(stock).data == {
            "id": stock.id,
            "available": stock.available,
            "country": stock.country,
            "discontinued": stock.discontinued,
            "price": "{:,.2f}".format(stock.price.amount),
            "price_currency": stock.price_currency,
            "quantity": stock.quantity,
            "source": stock.source,
            "title": stock.title,
            "url": stock.url,
            "history": [
                {
                    "price": "{:,.2f}".format(historic.price.amount),
                    "price_currency": historic.price_currency,
                    "modified": historic.modified.astimezone(
                        tz=get_current_timezone()
                    ).strftime(settings.REST_FRAMEWORK["DATETIME_FORMAT"]),
                }
                for historic in stock.history.all()
            ],
        }
