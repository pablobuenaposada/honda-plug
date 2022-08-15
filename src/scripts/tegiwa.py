from part.lambdas import add_stock
from part.models import Part
from scrapper.clients.tegiwa import TegiwaClient


def run():
    client = TegiwaClient()
    for part in Part.objects.stocked_parts_first().iterator():
        parsed_stock = client.get_part(part.reference)
        add_stock(parsed_stock)
