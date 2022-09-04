from part.constants import SOURCE_ACURAEXPRESSPARTS
from scrapper.clients.common import CommonClient


class AcuraexpresspartsClient(CommonClient):
    DOMAIN = "www.acuraexpressparts.com"
    SOURCE = SOURCE_ACURAEXPRESSPARTS
