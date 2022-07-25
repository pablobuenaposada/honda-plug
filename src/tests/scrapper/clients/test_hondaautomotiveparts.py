import pytest
from money import Money

from scrapper.clients.hondaautomotiveparts import HondaautomotivepartsClient
from scrapper.part.part import Part


@pytest.mark.vcr()
class TestHondaautomotivepartsClient:
    @pytest.mark.parametrize(
        "part_number, expected",
        (
            (
                "12251-RBB-004",
                Part(
                    available=True,
                    reference="12251-RBB-004",
                    price=Money(amount="98.65", currency="USD"),
                    title="Gasket, Cylinder Head (Nippon Leakless) - Honda (12251-RBB-004)",
                    discontinued=False,
                    image="https://dz310nzuyimx0.cloudfront.net/strapr1/7cfd97ab6173d165e37dec41c6a978e9/85957d0bd63c58860e15bdc7b79afe4f.gif",
                ),
            ),
            (
                "56483-PND-003",
                Part(
                    available=False,
                    reference="56483-PND-003",
                    price=Money(amount="15.82", currency="USD"),
                    title="Pulley, Power Steering Pump - Honda (56483-PND-003)",
                    discontinued=True,
                    image="https://dz310nzuyimx0.cloudfront.net/strapr1/056442089e514a4e09f554927e3d604f/7e1bbfa7e632ddb91eb5f5bb58518895.png",
                ),
            ),
        ),
    )
    def test_success(self, part_number, expected):
        assert HondaautomotivepartsClient().get_part(part_number) == expected
