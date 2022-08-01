from part.lambdas import add_part
from scrapper.clients.epcdata import EpcdataClient


def run():
    EpcdataClient().get_parts(add_part)
