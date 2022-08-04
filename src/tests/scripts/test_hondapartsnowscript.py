import pytest
from djmoney.money import Money
from model_bakery import baker

from part.constants import SOURCE_HONDAPARTSNOW
from part.models import Image, Part, Stock
from scripts.hondapartsnow import run


@pytest.mark.django_db
@pytest.mark.vcr()
class TestHondapartsnowScript:
    def test_script(self):
        part = baker.make(Part, reference="56483-PND-003")
        expected_stock = {
            "part": part,
            "title": "Pulley, Power Steering Pump",
            "source": SOURCE_HONDAPARTSNOW,
            "price": Money("15.68", "USD"),
            "available": False,
            "discontinued": True,
            "quantity": None,
            "url": "https://www.hondapartsnow.com/genuine/honda~pulley~power~steering~56483-pnd-003.html",
        }

        assert Stock.objects.count() == Image.objects.count() == 0
        run()
        assert Stock.objects.count() == Image.objects.count() == 1
        stock = Stock.objects.first()
        for field_name in {f.name for f in Stock._meta.get_fields()} - {
            "id",
            "created",
            "image",
            "modified",
            "price_currency",
        }:
            assert getattr(stock, field_name) == expected_stock[field_name]
        image = Image.objects.first()
        expected_image = {
            "stock": stock,
            "url": "https://www.hondapartsnow.com/resources/encry/part-picture/hpn/large/792b87b040876fda9770fd4a712d9665/756566f6e674b120a1c138fcb821a53c.png",
        }
        for field_name in {f.name for f in Image._meta.get_fields()} - {"id"}:
            assert getattr(image, field_name) == expected_image[field_name]
