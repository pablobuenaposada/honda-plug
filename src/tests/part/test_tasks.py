from unittest.mock import patch

import pytest
from model_bakery import baker

from part.constants import (
    SOURCE_ACURAEXPRESSPARTS,
    SOURCE_ACURAPARTSFORLESS,
    SOURCE_AKR,
    SOURCE_ALL4HONDA,
    SOURCE_AMAYAMA,
    SOURCE_CMS,
    SOURCE_HONDAAUTOMOTIVEPARTS,
    SOURCE_HONDAPARTSNOW,
    SOURCE_HONDAPARTSONLINE,
    SOURCE_HONDASPAREPARTS,
    SOURCE_JAPSERVICEPARTS,
    SOURCE_NENGUN,
    SOURCE_ONLINETEILE,
    SOURCE_PIECESAUTOHONDA,
    SOURCE_TEGIWA,
    SOURCE_UNKNOWN,
)
from part.models import Part, Stock
from part.tasks import CLIENTS, search_for_stocks

REFERENCE = "12251-RBB-004"


@pytest.mark.django_db
@pytest.mark.vcr()
class TestSearchForStocks:
    def test_success(self):
        assert Part.objects.count() == 0
        assert Stock.objects.count() == 0
        search_for_stocks(REFERENCE)
        assert Part.objects.count() == 1
        assert {stock.source for stock in Stock.objects.all()} == {
            "hondapartsnow",
            "hondapartsonline",
            "hondaautomotiveparts",
            "tegiwa",
            "hondaspareparts",
            "pieces-auto-honda",
            "amayama",
            "acuraexpressparts",
            "all4honda",
            "acurapartsforless",
            "cms",
            "akr",
            "online-teile",
        }

    @patch("part.tasks.search_for_stocks")
    def test_part_already_exists(self, m_search_for_stocks):
        baker.make(Part, reference=REFERENCE, source=SOURCE_UNKNOWN)
        assert Part.objects.count() == 1
        assert Stock.objects.count() == 0
        search_for_stocks(REFERENCE)
        assert Part.objects.count() == 1
        assert {stock.source for stock in Stock.objects.all()} == {
            "hondapartsnow",
            "hondapartsonline",
            "hondaautomotiveparts",
            "tegiwa",
            "hondaspareparts",
            "pieces-auto-honda",
            "amayama",
            "acuraexpressparts",
            "all4honda",
            "acurapartsforless",
            "cms",
            "akr",
            "online-teile",
        }

    @patch("part.tasks.search_for_stocks")
    def test_part_and_stock_already_exists(self, m_search_for_stocks):
        part = baker.make(Part, reference=REFERENCE, source=SOURCE_UNKNOWN)
        baker.make(Stock, part=part, source=SOURCE_HONDAPARTSNOW, country="US")
        baker.make(Stock, part=part, source=SOURCE_HONDAPARTSONLINE, country="US")
        baker.make(Stock, part=part, source=SOURCE_TEGIWA, country="GB")
        baker.make(Stock, part=part, source=SOURCE_HONDAAUTOMOTIVEPARTS, country="US")
        baker.make(Stock, part=part, source=SOURCE_HONDASPAREPARTS, country="GB")
        baker.make(Stock, part=part, source=SOURCE_PIECESAUTOHONDA, country="FR")
        baker.make(Stock, part=part, source=SOURCE_AMAYAMA, country="JP")
        baker.make(Stock, part=part, source=SOURCE_AMAYAMA, country="AE")
        baker.make(Stock, part=part, source=SOURCE_ACURAEXPRESSPARTS, country="US")
        baker.make(Stock, part=part, source=SOURCE_ALL4HONDA, country="NL")
        baker.make(Stock, part=part, source=SOURCE_ACURAPARTSFORLESS, country="US")
        baker.make(Stock, part=part, source=SOURCE_CMS, country="NL")
        baker.make(Stock, part=part, source=SOURCE_NENGUN, country="JP")
        baker.make(Stock, part=part, source=SOURCE_AKR, country="NL")
        baker.make(Stock, part=part, source=SOURCE_ONLINETEILE, country="DE")
        baker.make(Stock, part=part, source=SOURCE_JAPSERVICEPARTS, country="GB")

        assert Part.objects.count() == 1
        assert (
            Stock.objects.count() == len(CLIENTS) + 1
        )  # one more because amayama finds 2 more stocks
        search_for_stocks(REFERENCE)
        assert Part.objects.count() == 1
        assert {stock.source for stock in Stock.objects.all()} == {
            "nengun",
            "japserviceparts",
            "hondapartsnow",
            "hondapartsonline",
            "hondaautomotiveparts",
            "tegiwa",
            "hondaspareparts",
            "pieces-auto-honda",
            "amayama",
            "acuraexpressparts",
            "all4honda",
            "acurapartsforless",
            "cms",
            "akr",
            "online-teile",
        }

    @patch("part.tasks.search_for_stocks")
    @patch(
        "scrapper.clients.hondaautomotiveparts.HondaautomotivepartsClient.get_part",
        side_effect=Exception(),
    )
    def test_stock_exception(self, m_search_for_stocks, m_get_part):
        """
        If an exception is raised during getting the stock from a client,
        the rest of the clients should perform anyway.
        This test make hondaautomotiveparts client to fail but the rest should continue.
        """
        baker.make(Part, reference=REFERENCE, source=SOURCE_UNKNOWN)

        assert Part.objects.count() == 1
        assert Stock.objects.count() == 0
        search_for_stocks(REFERENCE)
        assert Part.objects.count() == 1
        assert {stock.source for stock in Stock.objects.all()} == {
            "hondapartsnow",
            "hondapartsonline",
            "tegiwa",
            "hondaspareparts",
            "pieces-auto-honda",
            "amayama",
            "acuraexpressparts",
            "all4honda",
            "acurapartsforless",
            "cms",
            "akr",
            "online-teile",
        }
