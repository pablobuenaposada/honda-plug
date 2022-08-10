import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from djmoney.money import Money
from model_bakery import baker

from part.constants import SOURCE_EPCDATA, SOURCE_HONDAPARTSNOW
from part.models import Image, Part, Stock


@pytest.mark.django_db
class TestPart:
    def test_unique(self):
        Part.objects.create(reference="56483-PND-003", source=SOURCE_EPCDATA)
        with pytest.raises(IntegrityError):
            Part.objects.create(reference="56483-PND-003", source=SOURCE_EPCDATA)

    def test_mandatory_fields(self):
        with pytest.raises(ValidationError) as error:
            Part.objects.create()
        assert "This field cannot be emtpy" in str(error.value)

    def test_reference_not_empty(self):
        with pytest.raises(ValidationError):
            Part.objects.create(reference="")

    def test_valid(self):
        data = {"reference": "56483-PND-003", "source": SOURCE_EPCDATA}
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


@pytest.mark.django_db
class TestStock:
    def test_unique(self):
        part = baker.make(Part, reference="56483-PND-003")
        baker.make(
            Stock, part=part, source=SOURCE_HONDAPARTSNOW, url="https://www.foo.com"
        )
        with pytest.raises(IntegrityError):
            baker.make(
                Stock, part=part, source=SOURCE_HONDAPARTSNOW, url="https://www.foo.com"
            )

    def test_mandatory_fields(self):
        with pytest.raises(IntegrityError) as error:
            Stock.objects.create()
        assert (
            'null value in column "part_id" of relation "part_stock" violates not-null constraint'
            in str(error.value)
        )

    def test_valid(self):
        part = baker.make(Part, reference="56483-PND-003")
        data = {
            "part": part,
            "title": "bar",
            "price": Money(1, "USD"),
            "available": True,
            "discontinued": False,
            "source": SOURCE_HONDAPARTSNOW,
            "quantity": 1,
            "url": "https://www.foo.com",
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
    def test_unique(self):
        part = baker.make(Part, reference="56483-PND-003")
        stock = baker.make(Stock, part=part, url="https://www.foo.com")
        Image.objects.create(stock=stock, url="http://www.foo.com")
        with pytest.raises(IntegrityError):
            Image.objects.create(stock=stock, url="http://www.foo.com")

    def test_mandatory_fields(self):
        with pytest.raises(ValidationError) as error:
            Image.objects.create()
        assert "This field cannot be emtpy" in str(error.value)

    def test_valid(self):
        part = baker.make(Part, reference="56483-PND-003")
        stock = baker.make(Stock, part=part, url="https://www.foo.com")
        data = {"stock": stock, "url": "http://www.foo.com"}
        image = Image.objects.create(**data)
        expected = data | {"id": image.id}

        for field in {field.name for field in Image._meta.get_fields()}:
            assert getattr(image, field) == expected[field]
