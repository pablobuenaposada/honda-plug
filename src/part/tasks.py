import asyncio
import logging

from django_rq import job
from sentry_sdk import capture_exception

from scrapper.clients.acuraexpressparts import AcuraexpresspartsClient
from scrapper.clients.acurapartsforless import AcurapartsforlessClient
from scrapper.clients.all4honda import All4hondaClient
from scrapper.clients.amayama import AmayamaClient
from scrapper.clients.cms import CmsClient
from scrapper.clients.hondaautomotiveparts import HondaautomotivepartsClient
from scrapper.clients.hondapartsnow import HondapartsnowClient
from scrapper.clients.hondapartsonline import HondapartsonlineClient
from scrapper.clients.hondaspareparts import HondasparepartsClient
from scrapper.clients.nengun import NengunClient
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
    All4hondaClient,
    AcurapartsforlessClient,
    CmsClient,
    NengunClient,
)


async def call_clients(reference):
    tasks = []
    for client in CLIENTS:
        tasks.append(client().get_part(reference))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    # flatten internal lists since some clients can return multiple Stocks
    return [y for x in results for y in (x if isinstance(x, list) else [x])]


@job
def search_for_stocks(reference):
    from part.lambdas import add_stock

    logger.info(f"Searching stocks for: {reference}")
    results = asyncio.run(call_clients(reference))
    for result in results:
        if type(result) == Exception:
            capture_exception(result)
        else:  # Stock instance
            try:
                add_stock(result)
            except Exception as e:
                capture_exception(e)
    logger.info(f"Done searching stocks for: {reference}")


@job
def enqueue_queryset(queryset):
    for part in queryset:
        search_for_stocks.delay(part.reference, at_front=True)
