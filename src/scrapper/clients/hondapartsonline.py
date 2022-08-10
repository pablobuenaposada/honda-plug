from part.constants import SOURCE_HONDAPARTSONLINE
from scrapper.clients.common import CommonClient


class HondapartsonlineClient(CommonClient):
    DOMAIN = "www.hondapartsonline.net"
    SOURCE = SOURCE_HONDAPARTSONLINE
