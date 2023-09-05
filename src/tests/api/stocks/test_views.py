from unittest.mock import patch

import pytest
from api.stocks.serializers import StockOutputSerializer
from django.contrib.auth.models import Permission, User
from django.shortcuts import resolve_url
from djmoney.money import Money
from model_bakery import baker
from part.constants import SOURCE_TEGIWA
from part.models import Part, Stock
from rest_framework import status
from rest_framework.authtoken.models import Token

REFERENCE = "56483-PND-003"


@pytest.mark.django_db
class TestsGetStocksView:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        with patch("part.models.search_for_stocks"):
            part = baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)
            self.stock = baker.make(
                Stock, part=part, source=SOURCE_TEGIWA, country="US"
            )

    def endpoint(self, pk):
        return resolve_url("api:stocks-detail", pk=pk)

    def test_url(self):
        assert self.endpoint(self.stock.id) == f"/api/stocks/{self.stock.pk}/"

    def test_success(self, client):
        response = client.get(self.endpoint(self.stock.pk))

        assert response.status_code == status.HTTP_200_OK
        assert response.data == StockOutputSerializer(self.stock).data


@pytest.mark.django_db
class TestsPostStocksView:
    endpoint = resolve_url("api:stocks-create")

    @pytest.fixture(autouse=True)
    def setup_class(self):
        user = baker.make(User)
        user.user_permissions.add(Permission.objects.get(name="Can add stock"))
        self.token = baker.make(Token, user=user)
        with patch("part.models.search_for_stocks"):
            self.part = baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)

    def test_url(self):
        assert self.endpoint == "/api/stocks/"

    def test_no_token(self, client):
        response = client.post(
            self.endpoint,
            {
                "part": self.part.pk,
                "title": "foo",
                "source": SOURCE_TEGIWA,
                "url": "https://www.foo.com",
                "country": "US",
                "price": "1.99",
                "price_currency": "USD",
            },
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_success(self, client):
        assert not Stock.objects.exists()
        response = client.post(
            self.endpoint,
            {
                "part": self.part.pk,
                "title": "foo",
                "source": SOURCE_TEGIWA,
                "url": "https://www.foo.com",
                "country": "US",
                "price": "1.99",
                "price_currency": "USD",
            },
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )

        assert response.status_code == status.HTTP_201_CREATED
        stock = Stock.objects.get()
        assert response.data == StockOutputSerializer(stock).data

    def test_success_update(self, client):
        """
        If stock already exists with same part, source and country the stock should be then updated
        """
        baker.make(
            Stock,
            part=self.part,
            source=SOURCE_TEGIWA,
            country="US",
            price=Money("0.99", "USD"),
        )
        assert Stock.objects.count() == 1
        modified_price = "1.99"
        response = client.post(
            self.endpoint,
            {
                "part": self.part.pk,
                "title": "foo",
                "source": SOURCE_TEGIWA,
                "url": "https://www.foo.com",
                "country": "US",
                "price": modified_price,
                "price_currency": "USD",
            },
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )

        assert response.status_code == status.HTTP_201_CREATED
        stock = Stock.objects.get()
        assert stock.history.count() == 2
        assert stock.price == Money(modified_price, "USD")
