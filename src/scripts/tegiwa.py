import logging

from sentry_sdk import capture_exception

from part.lambdas import add_stock
from part.models import Part
from scrapper.clients.tegiwa import TegiwaClient

logger = logging.getLogger(__name__)


def run():
    client = TegiwaClient()
    current = 0
    for part in Part.objects.stocked_parts_last().iterator():
        logger.info(f"Current:{current} Searching stocks for: {part.reference}")
        try:
            parsed_stock = client.get_part(part.reference)
            add_stock(parsed_stock)
        except Exception as e:
            capture_exception(e)
        logger.info(f"Done searching stocks for: {part.reference}")
        current += 1
