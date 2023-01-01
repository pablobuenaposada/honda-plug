from bs4 import BeautifulSoup
from money import Money

from part.constants import SOURCE_ICB
from scrapper.clients.interface import ClientInterface
from scrapper.common.stock import Stock


class IcbClient(ClientInterface):
    def get_parts(self):
        raise NotImplementedError

    async def get_part(self, reference):
        response, _, _ = await self.request_limiter.get(
            f"https://www.icbmotorsport.com/__lsearch/?q={reference}&storeid=yhst-1408381693991"
        )
        for result in response["results"]:
            if "honda of japan" in result["brand"].lower() and (
                reference in result["description"] or reference in result["title"]
            ):
                result_response, _, _ = await self.request_limiter.get(result["url"])
                soup = BeautifulSoup(result_response, "html.parser")
                available = (
                    True
                    if result["price"] != 0
                    or soup.find("input", {"class": "addtocartImg"})
                    else False
                )

                return Stock(
                    country="US",
                    url=result["url"],
                    reference=reference,
                    source=SOURCE_ICB,
                    title=result["title"],
                    available=available,
                    discontinued=None,
                    image=result["image"],
                    price=Money(result["price"], "USD"),
                )
