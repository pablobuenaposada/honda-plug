from unittest.mock import patch

import pytest
from api.parts.serializers import PartOutputSerializer, SearchOutputSerializer
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


@pytest.mark.django_db
@patch("part.models.search_for_stocks")
class TestsSearchView:
    endpoint = resolve_url("api:search")

    def test_url(self, m_search_for_stocks):
        assert self.endpoint == "/api/parts/"

    @pytest.mark.parametrize(
        "parts, search, expected_parts",
        (
            (["11111-PRB-000"], "", ["11111-PRB-000"]),
            (["11111-PRB-000"], "RRC", []),
            (["11111-PRB-000", "22222-RRC-000"], "RRC", ["22222-RRC-000"]),
            (["11111-PRB-000", "22222-RRC-000"], "2", ["22222-RRC-000"]),
            (["11111-PRB-000", "22222-RRC-000"], "1", ["11111-PRB-000"]),
            (["11111-PRB-000", "22222-RRC-000"], "12", []),
            (["11111-PRB-000", "22222-RRC-000"], "11111-RRC", []),
        ),
    )
    def test_success_part(
        self, m_search_for_stocks, client, parts, search, expected_parts
    ):
        for part in parts:
            baker.make(Part, reference=part, source=SOURCE_TEGIWA)

        response = client.get(self.endpoint, {"search": search})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"] == [
            SearchOutputSerializer(Part.objects.get(reference=part)).data
            for part in expected_parts
        ]

    @pytest.mark.parametrize(
        "parts, search, expected_parts",
        (
            (
                [
                    ("11111-PRB-000", "alternator"),
                ],
                "",
                ["11111-PRB-000"],
            ),
            (
                [
                    ("11111-PRB-000", "alternator"),
                ],
                "belt",
                [],
            ),
            (
                [
                    ("11111-PRB-000", "alternator"),
                ],
                "alternator",
                ["11111-PRB-000"],
            ),
            (
                [("11111-PRB-000", "alternator"), ("22222-RRC-000", "alternator")],
                "alternator",
                ["11111-PRB-000", "22222-RRC-000"],
            ),
        ),
    )
    def test_success_stock(
        self, m_search_for_stocks, client, parts, search, expected_parts
    ):
        for part in parts:
            part_created = baker.make(Part, reference=part[0], source=SOURCE_TEGIWA)
            baker.make(
                Stock,
                part=part_created,
                source=SOURCE_TEGIWA,
                country="US",
                title=part[1],
            )

        response = client.get(self.endpoint, {"search": search})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"] == [
            SearchOutputSerializer(Part.objects.get(reference=part)).data
            for part in expected_parts
        ]
