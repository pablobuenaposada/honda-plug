from part.constants import SOURCE_ACURAPARTSFORLESS
from scrapper.clients.common import CommonClient


class AcurapartsforlessClient(CommonClient):
    DOMAIN = "www.acurapartsforless.com"
    SOURCE = SOURCE_ACURAPARTSFORLESS
