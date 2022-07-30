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
        Part.objects.create(reference="56483-PND-003")
        with pytest.raises(IntegrityError):
            Part.objects.create(reference="56483-PND-003")

    def test_mandatory_fields(self):
        with pytest.raises(ValidationError, match="reference"):
            Part.objects.create()

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
        baker.make(Stock, part=part, source=SOURCE_HONDAPARTSNOW)
        with pytest.raises(IntegrityError):
            baker.make(Stock, part=part, source=SOURCE_HONDAPARTSNOW)

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
        stock = baker.make(Stock, part=part)
        Image.objects.create(stock=stock, url="http://www.foo.com")
        with pytest.raises(IntegrityError):
            Image.objects.create(stock=stock, url="http://www.foo.com")

    def test_mandatory_fields(self):
        with pytest.raises(IntegrityError) as error:
            Image.objects.create()
        assert (
            str(error.value)
            == 'null value in column "url" of relation "part_image" violates not-null constraint\nDETAIL:  Failing row contains (3, null, null).\n'
        )

    def test_valid(self):
        part = baker.make(Part, reference="56483-PND-003")
        stock = baker.make(Stock, part=part)
        data = {"stock": stock, "url": "http://www.foo.com"}
        image = Image.objects.create(**data)
        expected = data | {"id": image.id}

        for field in {field.name for field in Image._meta.get_fields()}:
            assert getattr(image, field) == expected[field]
