import pytest
from money import Money

from part.constants import (
    SOURCE_HONDAAUTOMOTIVEPARTS,
    SOURCE_HONDAPARTSNOW,
    SOURCE_HONDAPARTSONLINE,
    SOURCE_HONDASPAREPARTS,
    SOURCE_TEGIWA,
)
from scrapper.clients.hondaautomotiveparts import HondaautomotivepartsClient
from scrapper.clients.hondapartsnow import HondapartsnowClient
from scrapper.clients.hondapartsonline import HondapartsonlineClient
from scrapper.clients.hondaspareparts import HondasparepartsClient
from scrapper.clients.tegiwa import TegiwaClient
from scrapper.common.stock import Stock

REFERENCES = {
    "12251-RBB-004",  # normal part
    "56483-PND-003",  # discontinued part
    "08F03-S02-180K",  # really discontinued part
    "31206-P3F-003",  # sold out in some sites
}


@pytest.mark.vcr()
class TestClients:
    @pytest.mark.parametrize(
        "client, expected",
        (
            (
                HondapartsnowClient(),
                {
                    "12251-RBB-004": Stock(
                        available=True,
                        reference="12251-RBB-004",
                        price=Money(amount="102.08", currency="USD"),
                        title="Gasket, Cylinder Head (Nippon LEAkless)",
                        discontinued=False,
                        image="https://www.hondapartsnow.com/resources/encry/actual-picture/hpn/large/a5254ccaa3be7c7eb2b12f5745f04ca0/93bd5a06e83c3a33c1985cee27354789.jpg",
                        url="https://www.hondapartsnow.com/genuine/honda~gasket~cylinder~head~12251-rbb-004.html",
                        country="US",
                        source=SOURCE_HONDAPARTSNOW,
                    ),
                    "56483-PND-003": Stock(
                        available=False,
                        reference="56483-PND-003",
                        price=Money(amount="15.68", currency="USD"),
                        title="Pulley, Power Steering Pump",
                        discontinued=True,
                        image="https://www.hondapartsnow.com/resources/encry/part-picture/hpn/large/792b87b040876fda9770fd4a712d9665/756566f6e674b120a1c138fcb821a53c.png",
                        url="https://www.hondapartsnow.com/genuine/honda~pulley~power~steering~56483-pnd-003.html",
                        country="US",
                        source=SOURCE_HONDAPARTSNOW,
                    ),
                    "08F03-S02-180K": Stock(
                        available=False,
                        reference="08F03-S02-180K",
                        price=Money(amount="211.75", currency="USD"),
                        title="Spoiler, Rear Under (Vogue Silver Metallic)",
                        discontinued=True,
                        image=None,
                        url="https://www.hondapartsnow.com/genuine/honda~spoiler~08f03-s02-180k.html",
                        country="US",
                        source=SOURCE_HONDAPARTSNOW,
                    ),
                    "31206-P3F-003": Stock(
                        reference="31206-P3F-003",
                        url="https://www.hondapartsnow.com/genuine/honda~armature~31206-p3f-003.html",
                        source=SOURCE_HONDAPARTSNOW,
                        country="US",
                        title="Armature",
                        price=Money("365.23", "USD"),
                        image="https://www.hondapartsnow.com/resources/encry/part-picture/hpn/large/5045e7403da1abdff6fb3bebadf2b54b/8e3ec15302dc4429b6427e73d6984b06.png",
                        available=False,
                        discontinued=True,
                        quantity=None,
                    ),
                },
            ),
            (
                HondapartsonlineClient(),
                {
                    "12251-RBB-004": Stock(
                        available=True,
                        reference="12251-RBB-004",
                        price=Money(amount="107.23", currency="USD"),
                        title="Gasket, Cylinder Head (Nippon Leakless) - Honda (12251-RBB-004)",
                        discontinued=False,
                        image="https://dz310nzuyimx0.cloudfront.net/strapr1/7cfd97ab6173d165e37dec41c6a978e9/85957d0bd63c58860e15bdc7b79afe4f.gif",
                        url="https://www.hondapartsonline.net/search",
                        country="US",
                        source=SOURCE_HONDAPARTSONLINE,
                    ),
                    "56483-PND-003": Stock(
                        available=False,
                        reference="56483-PND-003",
                        price=Money(amount="16.48", currency="USD"),
                        title="Pulley, Power Steering Pump - Honda (56483-PND-003)",
                        discontinued=True,
                        image="https://dz310nzuyimx0.cloudfront.net/strapr1/056442089e514a4e09f554927e3d604f/7e1bbfa7e632ddb91eb5f5bb58518895.png",
                        url="https://www.hondapartsonline.net/search",
                        country="US",
                        source=SOURCE_HONDAPARTSONLINE,
                    ),
                    "08F03-S02-180K": Stock(
                        available=False,
                        reference="08F03-S02-180K",
                        price=Money(amount="220.58", currency="USD"),
                        title="Spoiler, Rear Under *NH583M* (Vogue Silver Metallic) - Honda (08F03-S02-180K)",
                        discontinued=True,
                        image="https://s3.amazonaws.com/static.revolutionparts.com/assets/images/honda.png",
                        url="https://www.hondapartsonline.net/search",
                        country="US",
                        source=SOURCE_HONDAPARTSONLINE,
                    ),
                    "31206-P3F-003": Stock(
                        reference="31206-P3F-003",
                        url="https://www.hondapartsonline.net/search",
                        source=SOURCE_HONDAPARTSONLINE,
                        country="US",
                        title="Armature - Honda (31206-P3F-003)",
                        price=Money(amount="380.45", currency="USD"),
                        image="https://dz310nzuyimx0.cloudfront.net/strapr1/9975b81af67056cae80ebf24ef8b639c/e20c8f426e887da8ac3ec1522cd66c31.gif",
                        available=True,
                        discontinued=False,
                        quantity=None,
                    ),
                },
            ),
            (
                HondaautomotivepartsClient(),
                {
                    "12251-RBB-004": Stock(
                        available=True,
                        reference="12251-RBB-004",
                        price=Money(amount="98.65", currency="USD"),
                        title="Gasket, Cylinder Head (Nippon Leakless) - Honda (12251-RBB-004)",
                        discontinued=False,
                        image="https://dz310nzuyimx0.cloudfront.net/strapr1/7cfd97ab6173d165e37dec41c6a978e9/85957d0bd63c58860e15bdc7b79afe4f.gif",
                        url="https://www.hondaautomotiveparts.com/search",
                        country="US",
                        source=SOURCE_HONDAAUTOMOTIVEPARTS,
                    ),
                    "56483-PND-003": Stock(
                        available=False,
                        reference="56483-PND-003",
                        price=Money(amount="15.82", currency="USD"),
                        title="Pulley, Power Steering Pump - Honda (56483-PND-003)",
                        discontinued=True,
                        image="https://dz310nzuyimx0.cloudfront.net/strapr1/056442089e514a4e09f554927e3d604f/7e1bbfa7e632ddb91eb5f5bb58518895.png",
                        url="https://www.hondaautomotiveparts.com/search",
                        country="US",
                        source=SOURCE_HONDAAUTOMOTIVEPARTS,
                    ),
                    "08F03-S02-180K": Stock(
                        available=False,
                        reference="08F03-S02-180K",
                        price=Money(amount="197.64", currency="USD"),
                        title="Spoiler, Rear Under *NH583M* (Vogue Silver Metallic) - Honda (08F03-S02-180K)",
                        discontinued=True,
                        image="https://s3.amazonaws.com/static.revolutionparts.com/assets/images/honda.png",
                        url="https://www.hondaautomotiveparts.com/search",
                        country="US",
                        source=SOURCE_HONDAAUTOMOTIVEPARTS,
                    ),
                    "31206-P3F-003": Stock(
                        reference="31206-P3F-003",
                        url="https://www.hondaautomotiveparts.com/search",
                        source=SOURCE_HONDAAUTOMOTIVEPARTS,
                        country="US",
                        title="Armature - Honda (31206-P3F-003)",
                        price=Money("340.88", currency="USD"),
                        image="https://dz310nzuyimx0.cloudfront.net/strapr1/9975b81af67056cae80ebf24ef8b639c/e20c8f426e887da8ac3ec1522cd66c31.gif",
                        available=True,
                        discontinued=False,
                        quantity=None,
                    ),
                },
            ),
            (
                TegiwaClient(),
                {
                    "12251-RBB-004": Stock(
                        available=False,
                        reference="12251-RBB-004",
                        price=Money(amount="65", currency="GBP"),
                        title="GENUINE HONDA HEAD GASKET K-SERIES K24",
                        discontinued=None,
                        url="https://www.tegiwaimports.com/genuine-honda-head-gasket-k-series-k24.html",
                        image="https://www.tegiwaimports.com/media/catalog/product/cache/1/image/470x470/4be6a58e18b1f94a8adc93cd75a4b5ce/g/e/genuine-honda-head-gasket-k-series_2.jpg",
                        country="GB",
                        source=SOURCE_TEGIWA,
                    ),
                    "56483-PND-003": None,
                    "08F03-S02-180K": None,
                    "31206-P3F-003": None,
                },
            ),
            (
                HondasparepartsClient(),
                {
                    "12251-RBB-004": Stock(
                        available=True,
                        reference="12251-RBB-004",
                        price=Money(amount="89.11", currency="GBP"),
                        title="GASKET COMP., CYLINDER HE",
                        discontinued=None,
                        url="https://hondaspareparts.co.uk/products/12251RBB004",
                        country="GB",
                        source=SOURCE_HONDASPAREPARTS,
                    ),
                    "56483-PND-003": Stock(
                        available=True,
                        reference="56483-PND-003",
                        price=Money(amount="74.47", currency="GBP"),
                        title="PULLEY COMP., POWER STEER",
                        discontinued=None,
                        url="https://hondaspareparts.co.uk/products/56483PND003",
                        country="GB",
                        source=SOURCE_HONDASPAREPARTS,
                    ),
                    "08F03-S02-180K": None,
                    "31206-P3F-003": Stock(
                        available=False,
                        reference="31206-P3F-003",
                        price=Money(amount="0.00", currency="GBP"),
                        title="ARMATURE COMP. (###)",
                        discontinued=None,
                        url="https://hondaspareparts.co.uk/products/31206P3F003",
                        country="GB",
                        source=SOURCE_HONDASPAREPARTS,
                    ),
                },
            ),
        ),
    )
    def test_success(self, client, expected):
        for reference in REFERENCES:
            assert client.get_part(reference) == expected[reference]
