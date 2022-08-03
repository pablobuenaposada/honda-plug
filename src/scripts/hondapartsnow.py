import logging
import time

from djmoney.money import Money

from part.constants import SOURCE_HONDAPARTSNOW
from part.models import Part, Stock
from scrapper.clients.hondapartsnow import HondapartsnowClient
from scripts.constants import WAIT_BETWEEN_REQUESTS


def run():
    logger = logging.getLogger(__name__)
    client = HondapartsnowClient()
    for part in Part.objects.all():
        try:
            time.sleep(WAIT_BETWEEN_REQUESTS)
            logger.info(f"searching {part.reference}")
            stock = client.get_part(part.reference)
        except Exception as error:
            logger.info(error)
        else:
            _, created = Stock.objects.update_or_create(
                part=part,
                title=stock.title,
                price=Money(stock.price.amount, stock.price.currency),
                available=stock.available,
                discontinued=stock.discontinued,
                source=SOURCE_HONDAPARTSNOW,
            )
            logger.info("added") if created else logger.info("updated")
