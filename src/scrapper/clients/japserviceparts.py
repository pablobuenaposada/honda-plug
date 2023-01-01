from bs4 import BeautifulSoup
from money import Money

from part.constants import SOURCE_JAPSERVICEPARTS
from scrapper.clients.interface import ClientInterface
from scrapper.common.stock import Stock


class JapservicepartsClient(ClientInterface):
    def get_parts(self):
        raise NotImplementedError

    async def get_part(self, reference):
        response, _, _ = await self.request_limiter.get(
            f"https://japserviceparts.co.uk/?wc-ajax=yith_ajax_search_products&query={reference}"
        )
        if response["suggestions"][0]["url"] == "":
            return

        for result in response["suggestions"]:
            item_response, _, _ = await self.request_limiter.get(result["url"])
            soup = BeautifulSoup(item_response, "html.parser")
            if (
                soup.find("meta", {"property": "product:retailer_item_id"})["content"]
                == reference
                and "genuine"
                in soup.find("meta", {"property": "og:description"})["content"].lower()
            ):
                price = soup.find("meta", {"property": "product:price:amount"})[
                    "content"
                ]
                currency = soup.find("meta", {"property": "product:price:currency"})[
                    "content"
                ]
                available = (
                    True
                    if soup.find("meta", {"property": "product:availability"})[
                        "content"
                    ]
                    == "instock"
                    else False
                )
                try:
                    quantity = soup.find("input", {"name": "quantity"})["max"]
                except (KeyError, TypeError):
                    if available:
                        quantity = 1
                    else:
                        quantity = None

                return Stock(
                    country="GB",
                    url=result["url"],
                    reference=reference,
                    source=SOURCE_JAPSERVICEPARTS,
                    title=soup.find("meta", {"property": "og:title"})["content"],
                    available=available,
                    discontinued=None,
                    image=soup.find("meta", {"property": "og:image"})["content"],
                    price=Money(price, currency),
                    quantity=quantity,
                )
