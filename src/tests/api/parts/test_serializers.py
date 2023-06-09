from unittest.mock import patch

import pytest
from api.parts.serializers import PartOutputSerializer, StockNestedOutputSerializer
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
