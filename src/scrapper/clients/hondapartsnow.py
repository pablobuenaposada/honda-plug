import json

from bs4 import BeautifulSoup
from money import Money

from part.constants import SOURCE_HONDAPARTSNOW
from scrapper.clients.interface import ClientInterface
from scrapper.common.stock import Stock


def _parse_availability(value):
    match value:
        case "http://schema.org/InStock":
            return True
        case "http://schema.org/Discontinued":
            return False
        case _:
            return None


def _is_discontinued(value):
    return True if value == "http://schema.org/Discontinued" else False


class HondapartsnowClient(ClientInterface):
    DOMAIN = "www.hondapartsnow.com"
    URL = f"https://{DOMAIN}/api/search/search-words"

    async def get_part(self, reference):
        response, _, _ = await self.request_limiter.get(
            self.URL, params={"searchText": reference}, headers={"site": "HPN"}
        )
        response, _, _ = await self.request_limiter.get(
            f'https://{self.DOMAIN}{response["data"]["redirectUrl"]}'
        )
        try:
            product_data = json.loads(
                BeautifulSoup(response, "html.parser")
                .findAll("script", {"data-react-helmet": "true"})[2]
                .contents[0]
            )
        except IndexError:
            return

        return Stock(
            country="US",
            source=SOURCE_HONDAPARTSNOW,
            reference=product_data["sku"],
            price=Money(amount=product_data["offers"]["price"], currency="USD"),
            title=product_data["description"],
            url=product_data["url"],
            available=_parse_availability(product_data["offers"]["availability"]),
            discontinued=_is_discontinued(product_data["offers"]["availability"]),
            image=None
            if not product_data.get("image", False)
            else product_data.get("image")[0],
        )

    def get_parts(self):
        raise NotImplementedError
