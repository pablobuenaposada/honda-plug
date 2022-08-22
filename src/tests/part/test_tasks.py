from unittest.mock import patch

import pytest
from model_bakery import baker

from part.constants import (
    SOURCE_HONDAAUTOMOTIVEPARTS,
    SOURCE_HONDAPARTSNOW,
    SOURCE_HONDAPARTSONLINE,
    SOURCE_HONDASPAREPARTS,
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
        assert Stock.objects.count() == len(CLIENTS)

    @patch("part.tasks.search_for_stocks")
    def test_part_already_exists(self, m_search_for_stocks):
        baker.make(Part, reference=REFERENCE, source=SOURCE_UNKNOWN)
        assert Part.objects.count() == 1
        assert Stock.objects.count() == 0
        search_for_stocks(REFERENCE)
        assert Part.objects.count() == 1
        assert Stock.objects.count() == len(CLIENTS)

    @patch("part.tasks.search_for_stocks")
    def test_part_and_stock_already_exists(self, m_search_for_stocks):
        part = baker.make(Part, reference=REFERENCE, source=SOURCE_UNKNOWN)
        baker.make(Stock, part=part, source=SOURCE_HONDAPARTSNOW, country="US")
        baker.make(Stock, part=part, source=SOURCE_HONDAPARTSONLINE, country="US")
        baker.make(Stock, part=part, source=SOURCE_TEGIWA, country="GB")
        baker.make(Stock, part=part, source=SOURCE_HONDAAUTOMOTIVEPARTS, country="US")
        baker.make(Stock, part=part, source=SOURCE_HONDASPAREPARTS, country="GB")
        assert Part.objects.count() == 1
        assert Stock.objects.count() == len(CLIENTS)
        search_for_stocks(REFERENCE)
        assert Part.objects.count() == 1
        assert Stock.objects.count() == len(CLIENTS)

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
        assert Stock.objects.count() == len(CLIENTS) - 1
