import logging
from datetime import datetime

from part.constants import SOURCE_TEGIWA
from part.models import Part
from scrapper.clients.tegiwa import TegiwaClient
from scripts.utils import add_stock

logger = logging.getLogger(__name__)


def run(*args):
    client = TegiwaClient()
    for part in Part.objects.all():
        log_message = (
            lambda message: f"{datetime.now()}: Part:{part.reference} {message}"
        )
        logger.info(log_message("..."))
        parsed_stock = client.get_part(part.reference)
        if parsed_stock:
            stock, created = add_stock(part, parsed_stock, SOURCE_TEGIWA)
            logger.info(log_message("added")) if created else logger.info(
                log_message("updated")
            )
        else:
            logger.info(log_message("not found"))
