import json

import requests
from bs4 import BeautifulSoup
from money import Money

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


class HondapartsnowClient:
    DOMAIN = "www.hondapartsnow.com"
    URL = f"https://{DOMAIN}/api/search/search-words"

    def get_part(self, part_number):
        response = requests.get(
            self.URL, params={"searchText": part_number}, headers={"site": "HPN"}
        )
        response.raise_for_status()
        response = response.json()

        response = requests.get(
            f'https://{self.DOMAIN}{response["data"]["redirectUrl"]}'
        )
        product_data = json.loads(
            BeautifulSoup(response.content, "html.parser")
            .findAll("script", {"data-react-helmet": "true"})[2]
            .contents[0]
        )

        return Stock(
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
