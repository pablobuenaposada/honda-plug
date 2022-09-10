import json

import requests
from bs4 import BeautifulSoup
from money import Money

from scrapper.clients.interface import ClientInterface
from scrapper.common.stock import Stock


def _parse_availability(value):
    match value:
        case "Available for Sale":
            return True
        case "Discontinued":
            return False
        case _:
            return None


def _is_discontinued(value):
    return True if value == "Discontinued" else False


class CommonClient(ClientInterface):
    SEARCH_SUFFIX = "/search"
    DOMAIN = ""
    SOURCE = ""

    async def get_part(self, reference):
        response, url, _ = await self.request_limiter.get(
            f"https://{self.DOMAIN}{self.SEARCH_SUFFIX}",
            params={"search_str": reference},
        )
        product_data = BeautifulSoup(response, "html.parser").find(id="product_data")
        if not product_data:  # this means that reference haven't been found
            return
        product_data = json.loads(product_data.contents[0])

        return Stock(
            country="US",
            source=self.SOURCE,
            reference=product_data["sku"],
            price=Money(amount=str(product_data["price"]), currency="USD"),
            title=product_data["title"],
            available=_parse_availability(product_data["current_product_availabilty"]),
            discontinued=_is_discontinued(product_data["current_product_availabilty"]),
            image=f'https://{product_data["images"][0]["main"]["url"][2:]}',
            url=str(url),
        )

    def get_parts(self):
        raise NotImplementedError
