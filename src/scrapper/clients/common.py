import json

import requests
from bs4 import BeautifulSoup
from money import Money

from scrapper.part.part import Part


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


class CommonClient:
    SEARCH_SUFFIX = "/search"
    DOMAIN = ""

    def get_part(self, part_number):
        response = requests.get(
            f"https://{self.DOMAIN}{self.SEARCH_SUFFIX}",
            params={"search_str": part_number},
        )
        response.raise_for_status()
        product_data = json.loads(
            BeautifulSoup(response.content, "html.parser")
            .find(id="product_data")
            .contents[0]
        )

        return Part(
            reference=product_data["sku"],
            price=Money(amount=str(product_data["price"]), currency="USD"),
            title=product_data["title"],
            available=_parse_availability(product_data["current_product_availabilty"]),
            discontinued=_is_discontinued(product_data["current_product_availabilty"]),
            image=f'https://{product_data["images"][0]["main"]["url"][2:]}',
        )
