import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from djmoney.money import Money
from model_bakery import baker

from part.models import Image, Part, Stock


@pytest.mark.django_db
class TestPart:
    def test_unique(self):
        Part.objects.create(reference="foo")
        with pytest.raises(IntegrityError):
            Part.objects.create(reference="foo")

    def test_mandatory_fields(self):
        with pytest.raises(IntegrityError, match="reference"):
            Part.objects.create()

    def test_reference_not_empty(self):
        with pytest.raises(ValidationError):
            Part.objects.create(reference="")

    def test_valid(self):
        data = {"reference": "foo"}
        part = Part.objects.create(**data)
        expected = data | {
            "id": part.id,
            "created": part.created,
            "modified": part.modified,
        }

        for field in [
            field.name
            for field in Part._meta.get_fields()
            if field.name not in ["stock"]
        ]:
            assert getattr(part, field) == expected[field]


@pytest.mark.django_db
class TestStock:
    def test_mandatory_fields(self):
        with pytest.raises(IntegrityError) as error:
            Stock.objects.create()
        assert str(error.value) == "NOT NULL constraint failed: part_stock.part_id"

    def test_valid(self):
        part = baker.make(Part, reference="foo")
        data = {
            "part": part,
            "title": "bar",
            "price": Money(1, "USD"),
            "available": True,
            "discontinued": False,
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


@pytest.mark.django_db
class TestImage:
    def test_mandatory_fields(self):
        with pytest.raises(IntegrityError) as error:
            Image.objects.create()
        assert str(error.value) == "NOT NULL constraint failed: part_image.url"

    def test_valid(self):
        part = baker.make(Part, reference="foo")
        stock = baker.make(Stock, part=part)
        data = {"stock": stock, "url": "http://www.foo.com"}
        image = Image.objects.create(**data)
        expected = data | {"id": image.id}

        for field in {field.name for field in Image._meta.get_fields()}:
            assert getattr(image, field) == expected[field]
