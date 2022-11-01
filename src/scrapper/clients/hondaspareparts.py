import json

import requests
from bs4 import BeautifulSoup
from money import Money
from price_parser import Price

from part.constants import SOURCE_HONDASPAREPARTS
from scrapper.clients.interface import ClientInterface
from scrapper.common.stock import Stock


class HondasparepartsClient(ClientInterface):
    async def get_part(self, reference):
        url = f'https://hondaspareparts.co.uk/products/{reference.replace("-", "")}'
        response, url, status_code = await self.request_limiter.get(url)

        if status_code != requests.codes.ok:
            return

        soup = BeautifulSoup(response, "html.parser")
        dict = json.loads(
            soup.find("script", {"id": "ProductJson-product-template"}).text
        )
        title = dict["title"].split("|")[0].strip()
        available = dict["available"]
        price = Price.fromstring(
            soup.find("meta", {"property": "og:price:amount"})["content"]
        )
        # their image seems is always a placeholder, so no image for now

        return Stock(
            reference=reference,
            available=available,
            url=str(url),
            source=SOURCE_HONDASPAREPARTS,
            country="GB",
            title=title,
            price=Money(price.amount, "GBP"),
        )

    def get_parts(self):
        raise NotImplementedError
