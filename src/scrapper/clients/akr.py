import json

from bs4 import BeautifulSoup
from money import Money
from part.constants import SOURCE_AKR
from price_parser import Price
from scrapper.clients.interface import ClientInterface
from scrapper.common.stock import Stock
from scrapper.utils import flatten_reference


class AkrClient(ClientInterface):
    def get_parts(self):
        raise NotImplementedError

    async def get_part(self, reference):
        search_response, _, _ = await self.request_limiter.post(
            "https://www.akr-performance.com/search/akr", data={"search": reference}
        )
        search_response = json.loads(search_response)
        url = None

        for result in search_response["products"]:
            if (
                flatten_reference(result["productOemNumber"])
                == flatten_reference(reference)
                and result["productBrand"] == "Honda"
            ):
                url = result["productUrl"]
                image = (
                    result["productImages"][0]["url"]
                    if len(result["productImages"]) > 0
                    else None
                )
                discontinued = (
                    True if int(result["productDiscontinued"]) == 1 else False
                )
                break
        if not url:
            return

        response, _, _ = await self.request_limiter.get(url)
        soup = BeautifulSoup(response, "html.parser")
        data = json.loads(soup.find("script", {"type": "application/ld+json"}).text)[1]

        available = None
        if data["offers"]["availability"] == "http://schema.org/BackOrder":
            available = False
        elif data["offers"]["availability"] == "http://schema.org/InStock":
            available = True
        return Stock(
            country="NL",
            url=url,
            reference=reference,
            source=SOURCE_AKR,
            title=data["name"],
            available=available,
            discontinued=discontinued,
            image=image,
            price=Money(
                Price.fromstring(data["offers"]["price"]).amount,
                data["offers"]["priceCurrency"],
            ),
        )
