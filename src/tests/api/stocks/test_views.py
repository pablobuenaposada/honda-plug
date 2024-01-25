import pytest
from api.stocks.serializers import StockBulkOutputSerializer, StockOutputSerializer
from django.contrib.auth.models import Permission, User
from django.shortcuts import resolve_url
from djmoney.money import Money
from model_bakery import baker
from part.constants import SOURCE_AMAYAMA, SOURCE_TEGIWA
from part.models import Part, Stock
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ErrorDetail
from review.models import ReviewPart

REFERENCE = "56483-PND-003"


@pytest.mark.django_db
class TestsStocksRetrieveView:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        part = baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)
        self.stock = baker.make(Stock, part=part, source=SOURCE_TEGIWA, country="US")

    def endpoint(self, pk):
        return resolve_url("api:stocks-detail", pk=pk)

    def test_url(self):
        assert self.endpoint(self.stock.id) == f"/api/stocks/{self.stock.pk}/"

    def test_success(self, client):
        response = client.get(self.endpoint(self.stock.pk))

        assert response.status_code == status.HTTP_200_OK
        assert response.data == StockOutputSerializer(self.stock).data


@pytest.mark.django_db
class TestsStocksCreateView:
    endpoint = resolve_url("api:stocks-create")

    @pytest.fixture(autouse=True)
    def setup_class(self):
        user = baker.make(User)
        user.user_permissions.add(Permission.objects.get(name="Can add stock"))
        self.token = baker.make(Token, user=user)
        self.part = baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)

    def test_url(self):
        assert self.endpoint == "/api/stocks/"

    def test_no_token(self, client):
        response = client.post(
            self.endpoint,
            {},
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
        assert Stock.objects.get().changed_by is None

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
        assert stock.changed_by == self.token.user

    def test_validation_error(self, client):
        response = client.post(
            self.endpoint,
            {
                "part": self.part.pk,
                "title": "foo",
                "source": SOURCE_TEGIWA,
                "url": "https://www.foo.com",
                "country": "foo",  # wrong country
                "price": "1.99",
                "price_currency": "USD",
            },
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "country": [
                ErrorDetail(
                    string='"foo" is not a valid choice.', code="invalid_choice"
                )
            ]
        }


@pytest.mark.django_db
class TestsStocksBulkCreateView:
    endpoint = resolve_url("api:stocks-bulk-create")

    @pytest.fixture(autouse=True)
    def setup_class(self):
        user = baker.make(User)
        user.user_permissions.add(Permission.objects.get(name="Can add stock"))
        self.token = baker.make(Token, user=user)
        self.part = baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)

    def test_url(self):
        assert self.endpoint == "/api/stocks/bulk/"

    def test_no_token(self, client):
        response = client.post(self.endpoint, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_success(self, client):
        assert not Stock.objects.exists()

        response = client.post(
            self.endpoint,
            [
                {
                    "reference": self.part.reference,
                    "title": "foo",
                    "source": SOURCE_TEGIWA,
                    "url": "https://www.foo.com",
                    "country": "US",
                    "price": "1",
                    "price_currency": "USD",
                },
                {
                    "reference": self.part.reference,
                    "title": "foo",
                    "source": SOURCE_AMAYAMA,
                    "url": "https://www.foo.com",
                    "country": "JP",
                    "price": "2",
                    "price_currency": "USD",
                },
            ],
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Stock.objects.count() == 2
        stock_tegiwa = Stock.objects.get(source=SOURCE_TEGIWA)
        stock_amayama = Stock.objects.get(source=SOURCE_AMAYAMA)
        assert stock_tegiwa.modified is not None
        assert stock_amayama.modified is not None
        serializer = StockBulkOutputSerializer(
            data={
                "created": 2,
                "duplicated": 0,
                "not_found": 0,
                "received": 2,
                "updated": 0,
                "errors": 0,
            }
        )
        serializer.is_valid()
        assert response.data == serializer.data
        assert not ReviewPart.objects.exists()

    def test_success_with_already_stock(self, client):
        stock = baker.make(Stock, part=self.part, source=SOURCE_TEGIWA, country="US")
        initial_modified_date = stock.modified
        response = client.post(
            self.endpoint,
            [
                {
                    "reference": REFERENCE,
                    "title": "foo",
                    "source": SOURCE_TEGIWA,
                    "url": "https://www.foo.com",
                    "country": "US",
                    "price": "1",
                    "price_currency": "USD",
                },
                {
                    "reference": REFERENCE,
                    "title": "foo",
                    "source": SOURCE_AMAYAMA,
                    "url": "https://www.foo.com",
                    "country": "JP",
                    "price": "2",
                    "price_currency": "USD",
                },
            ],
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Stock.objects.count() == 2
        stock_tegiwa = Stock.objects.get(source=SOURCE_TEGIWA)
        stock_amayama = Stock.objects.get(source=SOURCE_AMAYAMA)
        assert stock_tegiwa.history.count() == 2
        assert stock_amayama.history.count() == 1
        assert stock_tegiwa.modified > initial_modified_date
        assert stock_amayama.modified is not None
        serializer = StockBulkOutputSerializer(
            data={
                "created": 1,
                "duplicated": 0,
                "not_found": 0,
                "received": 2,
                "updated": 1,
                "errors": 0,
            }
        )
        serializer.is_valid()
        assert response.data == serializer.data
        assert not ReviewPart.objects.exists()

    def test_success_duplicated_stocks(self, client):
        assert not Stock.objects.exists()

        response = client.post(
            self.endpoint,
            [
                {
                    "reference": REFERENCE,
                    "title": "foo",
                    "source": SOURCE_TEGIWA,
                    "url": "https://www.foo.com",
                    "country": "US",
                    "price": "1",
                    "price_currency": "USD",
                },
                {
                    "reference": REFERENCE,
                    "title": "foo",
                    "source": SOURCE_TEGIWA,
                    "url": "https://www.foo.com",
                    "country": "US",
                    "price": "2",
                    "price_currency": "USD",
                },
            ],
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )

        assert response.status_code == status.HTTP_201_CREATED
        stocks = Stock.objects.all()
        assert stocks.count() == 1
        assert stocks[0].history.count() == 1
        assert stocks[0].modified is not None
        serializer = StockBulkOutputSerializer(
            data={
                "created": 1,
                "duplicated": 1,
                "not_found": 0,
                "received": 2,
                "updated": 0,
                "errors": 0,
            }
        )
        serializer.is_valid()
        assert response.data == serializer.data
        assert not ReviewPart.objects.exists()

    def test_success_without_part(self, client):
        assert not Stock.objects.exists()

        response = client.post(
            self.endpoint,
            [
                {
                    "reference": "1234-123-123",
                    "title": "foo",
                    "source": SOURCE_AMAYAMA,
                    "url": "https://www.foo.com",
                    "country": "JP",
                    "price": "2",
                    "price_currency": "USD",
                },
                {
                    "reference": REFERENCE,
                    "title": "foo",
                    "source": SOURCE_TEGIWA,
                    "url": "https://www.foo.com",
                    "country": "US",
                    "price": "1",
                    "price_currency": "USD",
                },
            ],
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )

        assert response.status_code == status.HTTP_201_CREATED
        stock = Stock.objects.get()
        assert stock.history.count() == 1
        assert stock.modified is not None
        serializer = StockBulkOutputSerializer(
            data={
                "created": 1,
                "duplicated": 0,
                "not_found": 1,
                "received": 2,
                "updated": 0,
                "errors": 0,
            }
        )
        serializer.is_valid()
        assert response.data == serializer.data
        assert ReviewPart.objects.get().reference == "1234-123-123"

    def test_partial_validation_error(self, client):
        assert not Stock.objects.exists()

        response = client.post(
            self.endpoint,
            [
                {
                    "reference": self.part.reference,
                    "title": "foo",
                    "source": SOURCE_TEGIWA,
                    "url": "https://www.foo.com",
                    "country": "US",
                    "price": "1",
                    "price_currency": "USD",
                },
                {
                    "reference": self.part.reference,
                    "title": "foo",
                    "source": SOURCE_AMAYAMA,
                    "url": "www.foo.com",
                    "country": "JP",
                    "price": "2",
                    "price_currency": "USD",
                },
            ],
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Stock.objects.exists() is False
        assert response.data == [
            {},
            {"url": [ErrorDetail(string="Enter a valid URL.", code="invalid")]},
        ]
        assert not ReviewPart.objects.exists()
