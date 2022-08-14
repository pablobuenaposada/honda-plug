import requests
from bs4 import BeautifulSoup
from money import Money
from price_parser import Price

from part.constants import SOURCE_HONDASPAREPARTS
from scrapper.clients.interface import ClientInterface
from scrapper.common.stock import Stock


class HondasparepartsClient(ClientInterface):
    def get_part(self, reference):
        url = f'https://hondaspareparts.co.uk/products/{reference.replace("-", "")}'
        response = self.request_limiter.get(url)

        if response.status_code != requests.codes.ok:
            return

        soup = BeautifulSoup(response.content, "html.parser")
        title = (
            soup.find("meta", {"property": "og:title"})["content"].split("|")[0].strip()
        )
        price = Price.fromstring(
            soup.find("meta", {"property": "og:price:amount"})["content"]
        )
        image = soup.find("meta", {"property": "og:image"})["content"]

        return Stock(
            reference=reference,
            url=url,
            source=SOURCE_HONDASPAREPARTS,
            country="GB",
            title=title,
            price=Money(price.amount, "GBP"),
            image=image,
        )

    def get_parts(self):
        raise NotImplemented
