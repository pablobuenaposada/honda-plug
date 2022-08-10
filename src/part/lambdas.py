import logging
from datetime import datetime

import pycountry
from djmoney.money import Money

from part.models import Part, Stock
from scrapper.common.stock import Stock as ParsedStock

logger = logging.getLogger(__name__)


def add_part(reference: str, source: str, message_prefix: str = ""):
    log_message = (
        lambda message: f"{datetime.now()}: {message_prefix} Part:{reference} {message}"
    )

    part, created = Part.objects.get_or_create(
        reference=reference,
        defaults={"reference": reference, "source": source},
    )
    if created:
        logger.info(log_message("added"))
    else:
        logger.info(log_message("already in"))
    return part


def add_stock(
    stock_parsed: ParsedStock,
    message_prefix: str = "",
):
    part = add_part(stock_parsed.reference, stock_parsed.source, message_prefix)
    log_message = (
        lambda message: f"{datetime.now()}: {message_prefix} Stock:{stock_parsed.reference} Source: {stock_parsed.source} Country: {pycountry.countries.get(alpha_2=stock_parsed.country).flag}  {message}"
    )
    stock, created = Stock.objects.update_or_create(
        part=part,
        source=stock_parsed.source,
        country=stock_parsed.country,
        defaults={
            "part": part,
            "title": stock_parsed.title,
            "price": Money(stock_parsed.price.amount, stock_parsed.price.currency)
            if stock_parsed.price is not None
            else None,
            "available": stock_parsed.available,
            "discontinued": stock_parsed.discontinued,
            "source": stock_parsed.source,
            "url": str(stock_parsed.url),
        },
    )
    logger.info(log_message("added")) if created else logger.info(
        log_message("updated")
    )
    # if stock.image:
    #     Image.objects.update_or_create(stock=stock, url=parsed_stock.image)
