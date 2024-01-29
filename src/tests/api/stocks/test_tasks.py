import pytest
from api.stocks.serializers import StockBulkInputSerializer
from api.stocks.tasks import bulk_create
from model_bakery import baker
from part.constants import SOURCE_AMAYAMA, SOURCE_TEGIWA
from part.models import Part, Stock
from review.models import ReviewPart

REFERENCE = "56483-PND-003"


@pytest.mark.django_db
class TestsBulkCreate:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.part = baker.make(Part, reference=REFERENCE, source=SOURCE_TEGIWA)

    def test_success(self):
        serializer = StockBulkInputSerializer(
            data=[
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
            many=True,
        )
        serializer.is_valid()
        bulk_create(serializer)

        assert Stock.objects.count() == 2
        stock_tegiwa = Stock.objects.get(source=SOURCE_TEGIWA)
        stock_amayama = Stock.objects.get(source=SOURCE_AMAYAMA)
        assert stock_tegiwa.modified is not None
        assert stock_amayama.modified is not None
        assert not ReviewPart.objects.exists()

    def test_success_with_already_stock(self, client):
        stock = baker.make(Stock, part=self.part, source=SOURCE_TEGIWA, country="US")
        initial_modified_date = stock.modified
        serializer = StockBulkInputSerializer(
            data=[
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
            many=True,
        )
        serializer.is_valid()
        bulk_create(serializer)

        assert Stock.objects.count() == 2
        stock_tegiwa = Stock.objects.get(source=SOURCE_TEGIWA)
        stock_amayama = Stock.objects.get(source=SOURCE_AMAYAMA)
        assert stock_tegiwa.history.count() == 2
        assert stock_amayama.history.count() == 1
        assert stock_tegiwa.modified > initial_modified_date
        assert stock_amayama.modified is not None
        assert not ReviewPart.objects.exists()

    def test_success_duplicated_stocks(self, client):
        assert not Stock.objects.exists()

        serializer = StockBulkInputSerializer(
            data=[
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
            many=True,
        )
        serializer.is_valid()
        bulk_create(serializer)

        stocks = Stock.objects.all()
        assert stocks.count() == 1
        assert stocks[0].history.count() == 1
        assert stocks[0].modified is not None
        assert not ReviewPart.objects.exists()

    def test_success_without_part(self, client):
        assert not Stock.objects.exists()

        serializer = StockBulkInputSerializer(
            data=[
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
            many=True,
        )
        serializer.is_valid()
        bulk_create(serializer)

        stock = Stock.objects.get()
        assert stock.history.count() == 1
        assert stock.modified is not None
        assert ReviewPart.objects.get().reference == "1234-123-123"
