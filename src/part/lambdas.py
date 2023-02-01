import logging
from datetime import datetime

import pycountry
from djmoney.money import Money
from scrapper.common.stock import Stock as ParsedStock
from scrapper.utils import flatten_reference

from part.models import Image, Part, Stock

logger = logging.getLogger(__name__)


def add_part(reference: str, source: str, message_prefix: str = ""):
    def log_message(message):
        return f"{datetime.now()}: {message_prefix} Part:{reference} {message}"

    try:
        # format the reference so the search ignores hyphens since they don't really matter for uniqueness
        regexp = flatten_reference(reference)
        regexp = [*regexp]
        regexp = "-?".join(regexp) + "$"

        part, created = Part.objects.get_or_create(
            reference__regex=regexp,
            defaults={"reference": reference, "source": source},
        )
    except Exception as error:
        logger.info(log_message(error))
        raise error
    if created:
        logger.info(log_message("added"))
    else:
        logger.info(log_message("already in"))
    return part


def add_stock(
    stock_parsed: ParsedStock,
    message_prefix: str = "",
):
    if not stock_parsed:
        return
    part = add_part(stock_parsed.reference, stock_parsed.source, message_prefix)

    def log_message(message):
        return f"{datetime.now()}: {message_prefix} Stock:{stock_parsed.reference} Source: {stock_parsed.source} Country: {pycountry.countries.get(alpha_2=stock_parsed.country).flag}  {message}"

    try:
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
                "quantity": stock_parsed.quantity,
            },
        )
    except Exception as error:
        logger.info(log_message(error))
        return error
    logger.info(log_message("added")) if created else logger.info(
        log_message("updated")
    )
    if stock_parsed.image:
        Image.objects.update_or_create(
            url=stock_parsed.image, defaults={"stock": stock, "url": stock_parsed.image}
        )
