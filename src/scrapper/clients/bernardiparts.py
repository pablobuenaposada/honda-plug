from bs4 import BeautifulSoup
from money import Money
from part.constants import SOURCE_BERNARDIPARTS
from scrapper.clients.interface import ClientInterface
from scrapper.common.stock import Stock


class BernardipartsClient(ClientInterface):
    def get_parts(self):
        raise NotImplementedError

    async def get_part(self, reference):
        response, url, _ = await self.request_limiter.get(
            "https://www.bernardiparts.com/Search.aspx",
            params={"keyword": reference},
        )
        soup = BeautifulSoup(response, "html.parser")
        price = soup.find("span", {"itemprop": "price"})
        if price:
            price = Money(amount=price["content"], currency="USD")
        image = (
            soup.find("img", {"itemprop": "image"})["src"]
            if soup.find("img", {"itemprop": "image"})["src"]
            != "/images/products/NoImageAvailable_m.jpg"
            else None
        )

        return Stock(
            country="US",
            source=SOURCE_BERNARDIPARTS,
            reference=reference,
            discontinued=True
            if soup.find("meta", {"itemprop": "availability"})["content"]
            == "Discontinued"
            else False,
            available=bool(
                soup.find(
                    "a", {"id": "ctl00_MainContentHolder_AddToCartButton1_btnAdd"}
                )
            ),
            price=price,
            title=soup.find("meta", {"property": "og:description"})["content"],
            url=soup.find("meta", {"property": "og:url"})["content"],
            image=image,
        )
