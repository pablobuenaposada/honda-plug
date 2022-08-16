from sentry_sdk import capture_exception

from part.lambdas import add_stock
from part.models import Part
from scrapper.clients.hondaspareparts import HondasparepartsClient


def run():
    client = HondasparepartsClient()
    for part in Part.objects.stocked_parts_first().iterator():
        try:
            parsed_stock = client.get_part(part.reference)
            add_stock(parsed_stock)
        except Exception as e:
            capture_exception(e)
