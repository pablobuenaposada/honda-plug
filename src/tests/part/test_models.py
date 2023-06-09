from unittest.mock import patch

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from djmoney.money import Money
from model_bakery import baker
from part.constants import SOURCE_EPCDATA, SOURCE_HONDAPARTSNOW, SOURCE_UNKNOWN
from part.models import Image, Part, Stock

REFERENCE = "56483-PND-003"


@pytest.mark.django_db
@patch("part.models.search_for_stocks")
class TestPart:
    def test_unique(self, m_search_for_stocks):
        Part.objects.create(reference=REFERENCE, source=SOURCE_EPCDATA)
        with pytest.raises(IntegrityError):
            Part.objects.create(reference=REFERENCE, source=SOURCE_EPCDATA)

        assert m_search_for_stocks.delay.call_count == 1

    def test_mandatory_fields(self, m_search_for_stocks):
        with pytest.raises(ValidationError) as error:
            Part.objects.create()

        assert "This field cannot be emtpy" in str(error.value)
        assert m_search_for_stocks.delay.call_count == 0

    def test_reference_not_empty(self, m_search_for_stocks):
        with pytest.raises(ValidationError):
            Part.objects.create(reference="")

        assert m_search_for_stocks.delay.call_count == 0

    def test_valid(self, m_search_for_stocks):
        data = {"reference": REFERENCE, "source": SOURCE_EPCDATA}
        part = Part.objects.create(**data)
        expected = data | {
            "id": part.id,
            "created": part.created,
            "modified": part.modified,
            "reference": data["reference"].upper(),
        }

        for field in [
            field.name
            for field in Part._meta.get_fields()
            if field.name not in ["stock"]
        ]:
            assert getattr(part, field) == expected[field]
        assert m_search_for_stocks.delay.call_count == 1

    def test_search_for_stocks(self, m_search_for_stocks):
        """
        Only new Parts should trigger a call to search_for_stocks
        """
        part = Part.objects.create(reference=REFERENCE, source=SOURCE_EPCDATA)
        assert m_search_for_stocks.delay.call_count == 1
        part.source = SOURCE_UNKNOWN
        part.save(update_fields=["source"])
        assert m_search_for_stocks.delay.call_count == 1


@pytest.mark.django_db
@patch("part.models.search_for_stocks")
class TestStock:
    def test_unique(self, m_search_for_stocks):
        part = baker.make(Part, reference=REFERENCE)
        Stock.objects.create(part=part, source=SOURCE_HONDAPARTSNOW, country="US")
        with pytest.raises(IntegrityError) as error:
            Stock.objects.create(part=part, source=SOURCE_HONDAPARTSNOW, country="US")

        assert "duplicate key value violates unique constraint" in str(error.value)
        assert m_search_for_stocks.delay.call_count == 1

    def test_mandatory_fields(self, m_search_for_stocks):
        with pytest.raises(IntegrityError) as error:
            Stock.objects.create()

        assert (
            'null value in column "part_id" of relation "part_stock" violates not-null constraint'
            in str(error.value)
        )
        assert m_search_for_stocks.delay.call_count == 0

    def test_valid(self, m_search_for_stocks):
        part = baker.make(Part, reference=REFERENCE)
        data = {
            "part": part,
            "title": "bar",
            "price": Money(1, "USD"),
            "available": True,
            "discontinued": False,
            "source": SOURCE_HONDAPARTSNOW,
            "quantity": 1,
            "url": "https://www.foo.com",
            "country": "US",
        }
        stock = Stock.objects.create(**data)
        expected = data | {
            "id": stock.id,
            "created": stock.created,
            "modified": stock.modified,
        }

        for field in {field.name for field in Stock._meta.get_fields()} - {
            "price_currency",
            "image",
        }:
            assert getattr(stock, field) == expected[field]
        assert m_search_for_stocks.delay.call_count == 1


@pytest.mark.django_db
@patch("part.models.search_for_stocks")
class TestImage:
    def test_unique(self, m_search_for_stocks):
        part = baker.make(Part, reference=REFERENCE)
        stock = baker.make(Stock, part=part, source=SOURCE_HONDAPARTSNOW, country="US")
        Image.objects.create(stock=stock, url="http://www.foo.com")
        with pytest.raises(IntegrityError) as error:
            Image.objects.create(stock=stock, url="http://www.foo.com")

        assert "duplicate key value violates unique constraint" in str(error.value)
        assert m_search_for_stocks.delay.call_count == 1

    def test_mandatory_fields(self, m_search_for_stocks):
        with pytest.raises(ValidationError) as error:
            Image.objects.create()

        assert "This field cannot be emtpy" in str(error.value)
        assert m_search_for_stocks.delay.call_count == 0

    def test_valid(self, m_search_for_stocks):
        part = baker.make(Part, reference=REFERENCE)
        stock = baker.make(Stock, part=part, source=SOURCE_HONDAPARTSNOW, country="US")
        data = {"stock": stock, "url": "http://www.foo.com"}
        image = Image.objects.create(**data)
        expected = data | {"id": image.id}

        for field in {field.name for field in Image._meta.get_fields()}:
            assert getattr(image, field) == expected[field]
        assert m_search_for_stocks.delay.call_count == 1
