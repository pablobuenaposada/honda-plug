import logging

from django_rq import job
from sentry_sdk import capture_exception

from scrapper.clients.acuraexpressparts import AcuraexpresspartsClient
from scrapper.clients.amayama import AmayamaClient
from scrapper.clients.hondaautomotiveparts import HondaautomotivepartsClient
from scrapper.clients.hondapartsnow import HondapartsnowClient
from scrapper.clients.hondapartsonline import HondapartsonlineClient
from scrapper.clients.hondaspareparts import HondasparepartsClient
from scrapper.clients.piecesautohonda import PiecesAutoHondaClient
from scrapper.clients.tegiwa import TegiwaClient

logger = logging.getLogger(__name__)
CLIENTS = (
    HondapartsnowClient,
    HondapartsonlineClient,
    HondaautomotivepartsClient,
    TegiwaClient,
    HondasparepartsClient,
    PiecesAutoHondaClient,
    AmayamaClient,
    AcuraexpresspartsClient,
)


@job
def search_for_stocks(reference):
    from part.lambdas import add_stock

    logger.info(f"Searching stocks for: {reference}")
    for client in CLIENTS:
        try:
            stocks = client().get_part(reference)
            if stocks:
                if type(stocks) == list:
                    for stock in stocks:
                        add_stock(stock)
                else:
                    add_stock(stocks)
            add_stock(stock)
        except Exception as e:
            capture_exception(e)
    logger.info(f"Done searching stocks for: {reference}")
