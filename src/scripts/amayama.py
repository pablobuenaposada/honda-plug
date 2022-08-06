from part.lambdas import add_part
from scrapper.clients.amayama import AmayamaClient


def run(*args):
    """
    If you want to start from a specific model you can pass the url of the model like this:
    python src/manage.py runscript amayama --script-args https://www.amayama.com/en/genuine-catalogs/honda/z
    """
    AmayamaClient().get_parts(add_part, args[0])
