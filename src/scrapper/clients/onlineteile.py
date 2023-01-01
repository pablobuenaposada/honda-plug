from bs4 import BeautifulSoup
from money import Money
from price_parser import Price

from part.constants import SOURCE_ONLINETEILE
from scrapper.clients.interface import ClientInterface
from scrapper.common.stock import Stock
from scrapper.utils import flatten_reference


class OnlineteileClient(ClientInterface):
    def get_parts(self):
        raise NotImplementedError

    async def get_part(self, reference):
        flattened_reference = flatten_reference(reference)
        response, _, _ = await self.request_limiter.get(
            f"https://www.online-teile.com/honda-ersatzteile/search_results.php?keywords={flattened_reference}&language=en"
        )
        soup = BeautifulSoup(response, "html.parser")
        results = soup.find_all("div", {"itemtype": "http://schema.org/Product"})
        for result in results:
            if (
                result.find("meta", {"itemprop": "sku"})["content"]
                == flattened_reference
            ):
                url = result.find("div", {"class": "cssButtonPos11"}).a["href"]
                response, _, _ = await self.request_limiter.get(f"{url}?language=en")
                soup = BeautifulSoup(response, "html.parser")
                if (
                    soup.find("img", {"itemprop": "image"})["src"]
                    != "https://www.online-teile.com/honda-ersatzteile/images/product_images/info_images/noimage.gif"
                ):
                    image = soup.find("img", {"itemprop": "image"})["src"]
                else:
                    image = None

                return Stock(
                    country="DE",
                    url=url,
                    reference=reference,
                    source=SOURCE_ONLINETEILE,
                    title=soup.find(id="mainpic")["title"],
                    available=True,
                    discontinued=None,
                    image=image,
                    price=Money(
                        Price.fromstring(
                            soup.find("meta", {"itemprop": "price"})["content"]
                        ).amount,
                        "EUR",
                    ),
                )
