import requests
from bs4 import BeautifulSoup
from money import Money

from scrapper.clients.interface import ClientInterface
from scrapper.common.stock import Stock
from scrapper.utils import RequestLimiter, string_to_float


def _parse_availability(soup):
    stock = soup.find(
        "span",
        {"class": lambda x: x and x.startswith("amstockstatus amsts_")},
    ).span["class"][0]
    match stock:
        case "mdb-non-stock":
            return False
        case "mdb-in-stock":
            return True
        case _:
            return None


class TegiwaClient(ClientInterface):
    def __init__(self):
        session = requests.Session()
        self.request_limiter = RequestLimiter(session)

    def get_part(self, part_number):
        response = self.request_limiter.get(
            "https://eucs4.klevu.com/cloud-search/n-search/search",
            params={
                "ticket": "klevu-14866558287345291",
                "term": part_number,
                "responseType": "json",
            },
        )

        for result in response.json()["result"]:
            response = self.request_limiter.get(
                result["url"], headers={"user-agent": "curl/7.79.1"}
            )
            soup = BeautifulSoup(response.content, "html.parser")
            sku = soup.find(id="sku").text
            if sku == part_number:
                return Stock(
                    reference=sku,
                    price=Money(
                        amount=string_to_float(
                            soup.find(
                                "span",
                                {
                                    "id": lambda L: L
                                    and L.startswith("price-including-tax-")
                                },
                            ).text
                        ),
                        currency="GBP",
                    ),
                    title=soup.find("div", {"class": "product-name"}).h1.text,
                    url=result["url"],
                    available=_parse_availability(soup),
                    image=soup.find(id="amasty_zoom")["src"],
                )
