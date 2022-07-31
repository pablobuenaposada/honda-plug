from scrapper.clients.epcdata import EpcdataClient

from part.lambdas import add_part


def run():
    EpcdataClient().get_parts(add_part)