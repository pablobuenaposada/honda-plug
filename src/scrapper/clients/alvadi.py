import re

from bs4 import BeautifulSoup
from money import Money

from part.constants import SOURCE_ALVADI
from scrapper.clients.interface import ClientInterface
from scrapper.common.stock import Stock
from scrapper.utils import flatten_reference


class AlvadiClient(ClientInterface):
    def get_parts(self):
        raise NotImplementedError

    async def get_part(self, reference):
        response, _, _ = await self.request_limiter.get(
            "https://alvadi.ee/en/search", params={"q": flatten_reference(reference)}
        )
        for result in BeautifulSoup(response, "html.parser").findAll(
            "a", {"class": "p-search-spare"}
        ):
            if result["href"].startswith("/en/original"):
                response_result, _, _ = await self.request_limiter.get(
                    f'https://alvadi.ee{result["href"]}'
                )
                soup = BeautifulSoup(response_result, "html.parser")

                return Stock(
                    country="EE",
                    source=SOURCE_ALVADI,
                    reference=reference,
                    available=True
                    if soup.find("meta", {"itemprop": "availability"})["content"]
                    == "InStock"
                    else False,
                    price=Money(
                        amount=soup.find("span", {"itemprop": "price"}).text,
                        currency="EUR",
                    ),
                    title=soup.find("td", text="Product")
                    .find_next_sibling("td")
                    .strong.text,
                    url=f'https://alvadi.ee{result["href"]}',
                    quantity=int(
                        re.search(
                            r"\d+",
                            soup.find(
                                "ul", {"class": "mb-0 list-inline list-inline-middle"}
                            ).strong.text,
                        ).group()
                    ),
                    image=soup.find("meta", {"property": "og:image"})["content"]
                    if soup.find("meta", {"property": "og:image"})["content"] != ""
                    else None,
                )
