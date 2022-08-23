import logging

from sentry_sdk import capture_exception

from part.lambdas import add_stock
from part.models import Part

logger = logging.getLogger(__name__)


class Config:
    client = None
    manager_method = "stocked_parts_last"


def run():
    client = Config.client()
    current = 0
    for part in getattr(Part.objects, Config.manager_method)().iterator():
        logger.info(f"Current:{current} Searching stocks for: {part.reference}")
        try:
            parsed_stock = client.get_part(part.reference)
            if parsed_stock:
                add_stock(parsed_stock)
        except Exception as e:
            capture_exception(e)
        logger.info(f"Done searching stocks for: {part.reference}")
        current += 1
