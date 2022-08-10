from part.constants import SOURCE_HONDAAUTOMOTIVEPARTS
from scrapper.clients.common import CommonClient


class HondaautomotivepartsClient(CommonClient):
    DOMAIN = "www.hondaautomotiveparts.com"
    SOURCE = SOURCE_HONDAAUTOMOTIVEPARTS
