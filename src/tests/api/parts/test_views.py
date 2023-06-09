from unittest.mock import patch

import pytest
from api.parts.serializers import PartOutputSerializer
from django.shortcuts import resolve_url
from model_bakery import baker
from part.constants import SOURCE_TEGIWA
from part.models import Part, Stock
from rest_framework import status

REFERENCE = "56483-PND-003"


@pytest.mark.django_db
@patch("part.models.search_for_stocks")
class TestsPartsView:
    def endpoint(self, reference):
        return resolve_url("api:parts-detail", reference=reference)

    def test_url(self, m_search_for_stocks):
        baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)

        assert self.endpoint(REFERENCE.lower()) == f"/api/parts/{REFERENCE.lower()}/"

    def test_success(self, m_search_for_stocks, client):
        part = baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)
        baker.make(Stock, part=part, source=SOURCE_TEGIWA, country="US")
        response = client.get(self.endpoint(REFERENCE.lower()))

        assert response.status_code == status.HTTP_200_OK
        assert response.data == PartOutputSerializer(part).data
