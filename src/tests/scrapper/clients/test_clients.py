import pytest
from money import Money

from scrapper.clients.hondaautomotiveparts import HondaautomotivepartsClient
from scrapper.clients.hondapartsnow import HondapartsnowClient
from scrapper.clients.hondapartsonline import HondapartsonlineClient
from scrapper.clients.tegiwa import TegiwaClient
from scrapper.part.part import Part

REFERENCES = {
    "12251-RBB-004",  # normal part
    "56483-PND-003",  # discontinued part
}


@pytest.mark.vcr()
class TestClients:
    @pytest.mark.parametrize(
        "client, expected",
        (
            (
                HondapartsnowClient(),
                {
                    "12251-RBB-004": Part(
                        available=True,
                        reference="12251-RBB-004",
                        price=Money(amount="102.08", currency="USD"),
                        title="Gasket, Cylinder Head (Nippon LEAkless)",
                        discontinued=False,
                        image="https://www.hondapartsnow.com/resources/encry/actual-picture/hpn/large/a5254ccaa3be7c7eb2b12f5745f04ca0/93bd5a06e83c3a33c1985cee27354789.jpg",
                        url="https://www.hondapartsnow.com/genuine/honda~gasket~cylinder~head~12251-rbb-004.html",
                    ),
                    "56483-PND-003": Part(
                        available=False,
                        reference="56483-PND-003",
                        price=Money(amount="15.68", currency="USD"),
                        title="Pulley, Power Steering Pump",
                        discontinued=True,
                        image="https://www.hondapartsnow.com/resources/encry/part-picture/hpn/large/792b87b040876fda9770fd4a712d9665/756566f6e674b120a1c138fcb821a53c.png",
                        url="https://www.hondapartsnow.com/genuine/honda~pulley~power~steering~56483-pnd-003.html",
                    ),
                },
            ),
            (
                HondapartsonlineClient(),
                {
                    "12251-RBB-004": Part(
                        available=True,
                        reference="12251-RBB-004",
                        price=Money(amount="107.23", currency="USD"),
                        title="Gasket, Cylinder Head (Nippon Leakless) - Honda (12251-RBB-004)",
                        discontinued=False,
                        image="https://dz310nzuyimx0.cloudfront.net/strapr1/7cfd97ab6173d165e37dec41c6a978e9/85957d0bd63c58860e15bdc7b79afe4f.gif",
                        url="https://www.hondapartsonline.net/search",
                    ),
                    "56483-PND-003": Part(
                        available=False,
                        reference="56483-PND-003",
                        price=Money(amount="16.48", currency="USD"),
                        title="Pulley, Power Steering Pump - Honda (56483-PND-003)",
                        discontinued=True,
                        image="https://dz310nzuyimx0.cloudfront.net/strapr1/056442089e514a4e09f554927e3d604f/7e1bbfa7e632ddb91eb5f5bb58518895.png",
                        url="https://www.hondapartsonline.net/search",
                    ),
                },
            ),
            (
                HondaautomotivepartsClient(),
                {
                    "12251-RBB-004": Part(
                        available=True,
                        reference="12251-RBB-004",
                        price=Money(amount="98.65", currency="USD"),
                        title="Gasket, Cylinder Head (Nippon Leakless) - Honda (12251-RBB-004)",
                        discontinued=False,
                        image="https://dz310nzuyimx0.cloudfront.net/strapr1/7cfd97ab6173d165e37dec41c6a978e9/85957d0bd63c58860e15bdc7b79afe4f.gif",
                        url="https://www.hondaautomotiveparts.com/search",
                    ),
                    "56483-PND-003": Part(
                        available=False,
                        reference="56483-PND-003",
                        price=Money(amount="15.82", currency="USD"),
                        title="Pulley, Power Steering Pump - Honda (56483-PND-003)",
                        discontinued=True,
                        image="https://dz310nzuyimx0.cloudfront.net/strapr1/056442089e514a4e09f554927e3d604f/7e1bbfa7e632ddb91eb5f5bb58518895.png",
                        url="https://www.hondaautomotiveparts.com/search",
                    ),
                },
            ),
            (
                TegiwaClient(),
                {
                    "12251-RBB-004": Part(
                        available=False,
                        reference="12251-RBB-004",
                        price=Money(amount="65", currency="GBP"),
                        title="GENUINE HONDA HEAD GASKET K-SERIES K24",
                        discontinued=None,
                        url="https://www.tegiwaimports.com/genuine-honda-head-gasket-k-series-k24.html",
                        image="https://www.tegiwaimports.com/media/catalog/product/cache/1/image/470x470/4be6a58e18b1f94a8adc93cd75a4b5ce/g/e/genuine-honda-head-gasket-k-series_2.jpg",
                    ),
                    "56483-PND-003": None,
                },
            ),
        ),
    )
    def test_success(self, client, expected):
        for reference in REFERENCES:
            assert client.get_part(reference) == expected[reference]
