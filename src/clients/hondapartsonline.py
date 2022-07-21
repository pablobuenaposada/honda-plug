import json

import requests
from bs4 import BeautifulSoup
from money import Money


def _parse_availability(value):
    # TODO: change by new switch python syntax
    if value == "Available for Sale":
        return True
    elif value == "Discontinued":
        return False
    else:
        return None


def _is_discontinued(value):
    return True if value == "Discontinued" else False


class HondapartsonlineClient:
    URL = "https://www.hondapartsonline.net/search"

    def get_part(self, part_number):
        response = requests.get(self.URL, params={"search_str": part_number})
        response.raise_for_status()
        product_data = json.loads(
            BeautifulSoup(response.content, "html.parser")
            .find(id="product_data")
            .contents[0]
        )
        return {
            "part_number": product_data["sku"],
            "price": Money(amount=product_data["price"], currency="USD"),
            "title": product_data["title"],
            "available": _parse_availability(
                product_data["current_product_availabilty"]
            ),
            "discontinued": _is_discontinued(
                product_data["current_product_availabilty"]
            ),
            "image": product_data["images"][0]["main"]["url"][2:],
        }
