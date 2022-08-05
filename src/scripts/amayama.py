from part.lambdas import add_part
from scrapper.clients.amayama import AmayamaClient


def run():
    AmayamaClient().get_parts(add_part)
