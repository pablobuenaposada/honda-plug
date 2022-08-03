import pytest
from djmoney.money import Money
from model_bakery import baker

from part.constants import SOURCE_HONDAPARTSNOW
from part.models import Part, Stock
from scripts.hondapartsnow import run


@pytest.mark.django_db
@pytest.mark.vcr()
class TestHondapartsnowScript:
    def test_script(self):
        part = baker.make(Part, reference="56483-PND-003")
        expected = {
            "part": part,
            "title": "Pulley, Power Steering Pump",
            "source": SOURCE_HONDAPARTSNOW,
            "price": Money("15.68", "USD"),
            "available": False,
            "discontinued": True,
            "quantity": None,
        }

        assert Stock.objects.count() == 0
        run()
        assert Stock.objects.count() == 1
        stock = Stock.objects.first()
        for field_name in {f.name for f in Stock._meta.get_fields()} - {
            "id",
            "created",
            "image",
            "modified",
            "price_currency",
        }:
            assert getattr(stock, field_name) == expected[field_name]
