import logging
import time
from datetime import datetime

from djmoney.money import Money

from part.constants import SOURCE_HONDAPARTSNOW
from part.models import Image, Part, Stock
from scrapper.clients.hondapartsnow import HondapartsnowClient
from scripts.constants import WAIT_BETWEEN_REQUESTS


def run():
    logger = logging.getLogger(__name__)
    client = HondapartsnowClient()
    logger.info(f"START")
    for part in Part.objects.all():
        try:
            time.sleep(WAIT_BETWEEN_REQUESTS)
            logger.info(f"{datetime.now()}: searching {part.reference}")
            parsed_stock = client.get_part(part.reference)
        except Exception as error:
            logger.info(error)
        else:
            stock, created = Stock.objects.update_or_create(
                part=part,
                source=SOURCE_HONDAPARTSNOW,
                defaults={
                    "part": part,
                    "title": parsed_stock.title,
                    "price": Money(
                        parsed_stock.price.amount, parsed_stock.price.currency
                    ),
                    "available": parsed_stock.available,
                    "discontinued": parsed_stock.discontinued,
                    "source": SOURCE_HONDAPARTSNOW,
                    "url": parsed_stock.url,
                    "country": "US",
                },
            )
            logger.info("added") if created else logger.info("updated")
            if parsed_stock.image:
                Image.objects.update_or_create(stock=stock, url=parsed_stock.image)
    logger.info(f"FINISH")
