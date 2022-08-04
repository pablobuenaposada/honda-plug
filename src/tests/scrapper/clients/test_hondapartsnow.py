import pytest
from money import Money

from scrapper.clients.hondapartsnow import HondapartsnowClient
from scrapper.part.part import Part


@pytest.mark.vcr()
class TestHondapartsnowClient:
    @pytest.mark.parametrize(
        "part_number, expected",
        (
            (
                "12251-RBB-004",
                Part(
                    available=True,
                    reference="12251-RBB-004",
                    price=Money(amount="102.08", currency="USD"),
                    title="Gasket, Cylinder Head (Nippon LEAkless)",
                    discontinued=False,
                    image="https://www.hondapartsnow.com/resources/encry/actual-picture/hpn/large/a5254ccaa3be7c7eb2b12f5745f04ca0/93bd5a06e83c3a33c1985cee27354789.jpg",
                    url="https://www.hondapartsnow.com/genuine/honda~gasket~cylinder~head~12251-rbb-004.html",
                ),
            ),
            (
                "56483-PND-003",
                Part(
                    available=False,
                    reference="56483-PND-003",
                    price=Money(amount="15.68", currency="USD"),
                    title="Pulley, Power Steering Pump",
                    discontinued=True,
                    image="https://www.hondapartsnow.com/resources/encry/part-picture/hpn/large/792b87b040876fda9770fd4a712d9665/756566f6e674b120a1c138fcb821a53c.png",
                    url="https://www.hondapartsnow.com/genuine/honda~pulley~power~steering~56483-pnd-003.html",
                ),
            ),
            (
                "72861-SEA-J00",
                Part(
                    available=False,
                    reference="72861-SEA-J00",
                    price=Money(amount="0.00", currency="USD"),
                    title="Seal, L. RR. Door Hole",
                    discontinued=True,
                    image=None,
                    url="https://www.hondapartsnow.com/genuine/honda~seal~72861-sea-j00.html",
                ),
            ),
        ),
    )
    def test_success(self, part_number, expected):
        assert HondapartsnowClient().get_part(part_number) == expected
