import logging

from django_rq import job

from scrapper.clients.hondaautomotiveparts import HondaautomotivepartsClient
from scrapper.clients.hondapartsnow import HondapartsnowClient
from scrapper.clients.hondapartsonline import HondapartsonlineClient
from scrapper.clients.hondaspareparts import HondasparepartsClient
from scrapper.clients.tegiwa import TegiwaClient

logger = logging.getLogger(__name__)
CLIENTS = (
    HondapartsnowClient,
    HondapartsonlineClient,
    HondaautomotivepartsClient,
    TegiwaClient,
    HondasparepartsClient,
)


@job
def search_for_stocks(reference):
    from part.lambdas import add_stock

    logger.info(f"Searching stocks for: {reference}")
    for client in CLIENTS:
        stock = client().get_part(reference)
        add_stock(stock)
