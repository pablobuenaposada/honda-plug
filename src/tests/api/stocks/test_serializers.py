from unittest.mock import patch

import pytest
from api.parts.serializers import HistoricalStockNestedOutputSerializer
from api.stocks.serializers import (
    ImageNestedOutputSerializer,
    StockInputSerializer,
    StockOutputSerializer,
)
from django.conf import settings
from django.utils.timezone import get_current_timezone
from djmoney.money import Money
from model_bakery import baker
from part.constants import SOURCE_TEGIWA
from part.models import Image, Part, Stock
from rest_framework.exceptions import ErrorDetail

REFERENCE = "56483-PND-003"


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
class TestsImageNestedOutputSerializer:
    serializer_class = ImageNestedOutputSerializer

    def test_success(self, m_search_for_stocks):
        part = baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)
        stock = baker.make(Stock, part=part, source=SOURCE_TEGIWA, country="US")
        image = baker.make(Image, stock=stock, url="http://www.foo.com")

        assert self.serializer_class(image).data == {"url": image.url}


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
        image = baker.make(Image, stock=stock, url="http://www.foo.com")

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
            "images": [ImageNestedOutputSerializer(image).data],
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


@pytest.mark.django_db
class TestStockInputSerializer:
    serializer_class = StockInputSerializer

    @pytest.fixture(autouse=True)
    def setup_class(self):
        with patch("part.models.search_for_stocks"):
            self.part = baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)

    def test_mandatory(self):
        serializer = self.serializer_class(data={})

        assert not serializer.is_valid()
        assert serializer.errors == {
            "part": [ErrorDetail(string="This field is required.", code="required")],
            "title": [ErrorDetail(string="This field is required.", code="required")],
            "source": [ErrorDetail(string="This field is required.", code="required")],
            "url": [ErrorDetail(string="This field is required.", code="required")],
            "country": [ErrorDetail(string="This field is required.", code="required")],
        }

    def test_success_min(self):
        serializer = self.serializer_class(
            data={
                "part": self.part.pk,
                "title": "foo",
                "source": SOURCE_TEGIWA,
                "url": "https://www.foo.com",
                "country": "US",
            }
        )

        assert serializer.is_valid()
        assert serializer.validated_data == {
            "part": self.part,
            "country": "US",
            "source": SOURCE_TEGIWA,
            "title": "foo",
            "url": "https://www.foo.com",
        }

    def test_success_full(self):
        serializer = self.serializer_class(
            data={
                "part": self.part.pk,
                "title": "foo",
                "source": SOURCE_TEGIWA,
                "url": "https://www.foo.com",
                "country": "US",
                "available": True,
                "discontinued": False,
                "price": Money("1.90", "EUR"),
                "quantity": 1,
            }
        )

        assert serializer.is_valid()
        assert serializer.validated_data == {
            "part": self.part,
            "country": "US",
            "source": SOURCE_TEGIWA,
            "title": "foo",
            "url": "https://www.foo.com",
            "available": True,
            "discontinued": False,
            "price": Money("1.90", "EUR"),
            "quantity": 1,
        }
