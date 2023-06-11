from unittest.mock import patch

import pytest
from api.stocks.serializers import StockOutputSerializer
from django.shortcuts import resolve_url
from model_bakery import baker
from part.constants import SOURCE_TEGIWA
from part.models import Part, Stock
from rest_framework import status

REFERENCE = "56483-PND-003"


@pytest.mark.django_db
@patch("part.models.search_for_stocks")
class TestsStocksView:
    def endpoint(self, pk):
        return resolve_url("api:stocks-detail", pk=pk)

    def test_url(self, m_search_for_stocks):
        part = baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)
        stock = baker.make(Stock, part=part, source=SOURCE_TEGIWA, country="US")

        assert self.endpoint(stock.id) == f"/api/stocks/{stock.pk}/"

    def test_success(self, m_search_for_stocks, client):
        part = baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)
        stock = baker.make(Stock, part=part, source=SOURCE_TEGIWA, country="US")
        response = client.get(self.endpoint(stock.pk))

        assert response.status_code == status.HTTP_200_OK
        assert response.data == StockOutputSerializer(stock).data
