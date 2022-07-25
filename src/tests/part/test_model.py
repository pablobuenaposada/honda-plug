import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from model_bakery import baker

from part.models import Part, Stock


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
        with pytest.raises(IntegrityError):
            Stock.objects.create()

    def test_valid(self):
        part = baker.make(Part, reference="foo")
        data = {"reference": part, "title": "bar"}
        stock = Stock.objects.create(**data)
        expected = data | {
            "id": stock.id,
            "created": stock.created,
            "modified": stock.modified,
        }

        for field in [field.name for field in Stock._meta.get_fields()]:
            assert getattr(stock, field) == expected[field]
