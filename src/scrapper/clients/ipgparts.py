from bs4 import BeautifulSoup
from money import Money

from part.constants import SOURCE_IPGPARTS
from scrapper.clients.interface import ClientInterface
from scrapper.common.stock import Stock


class IpgpartsClient(ClientInterface):
    def get_parts(self):
        raise NotImplementedError

    async def get_part(self, reference):
        response, _, _ = await self.request_limiter.get(
            "https://ipgparts.com/search",
            params={
                "q": reference,
            },
        )
        for result in BeautifulSoup(response, "html.parser").findAll(
            "h2", {"class": "h3"}
        ):
            url = f'https://ipgparts.com{result.a["href"]}'
            response, _, _ = await self.request_limiter.get(url)
            soup = BeautifulSoup(response, "html.parser")
            sku = soup.find("option", {"selected": "selected"})["data-sku"]

            if sku == reference:
                return Stock(
                    country="US",
                    source=SOURCE_IPGPARTS,
                    reference=reference,
                    price=Money(
                        amount=soup.find("meta", {"property": "og:price:amount"})[
                            "content"
                        ],
                        currency="USD",
                    ),
                    title=soup.find("meta", {"property": "og:title"})["content"],
                    url=url,
                    image=soup.find("meta", {"property": "og:image:secure_url"})[
                        "content"
                    ],
                )
