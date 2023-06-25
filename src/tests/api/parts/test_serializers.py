from unittest.mock import patch

import pytest
from api.parts.serializers import (
    PartOutputSerializer,
    SearchOutputSerializer,
    StockNestedOutputSerializer,
)
from model_bakery import baker
from part.constants import SOURCE_HONDAPARTSNOW, SOURCE_HONDASPAREPARTS, SOURCE_TEGIWA
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
            "title": None,
        }

    def test_success_with_stocks(self, m_search_for_stocks):
        part = baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)
        baker.make(
            Stock,
            part=part,
            source=SOURCE_HONDAPARTSNOW,
            country="US",
        )
        stock = baker.make(
            Stock,
            part=part,
            source=SOURCE_HONDASPAREPARTS,
            country="US",
        )

        assert self.serializer_class(part).data == {
            "reference": part.reference,
            "stock": [
                StockNestedOutputSerializer(stock).data
                for stock in part.stock_set.all()
            ],
            "title": stock.title,
        }


@pytest.mark.django_db
@patch("part.models.search_for_stocks")
class TestsSearchOutputSerializer:
    serializer_class = SearchOutputSerializer

    def test_success(self, m_search_for_stocks):
        part = baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)

        assert self.serializer_class(part).data == {
            "reference": part.reference,
        }