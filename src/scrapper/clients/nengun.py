import json

from bs4 import BeautifulSoup
from money import Money
from part.constants import SOURCE_NENGUN
from scrapper.clients.interface import ClientInterface
from scrapper.common.stock import Stock
from scrapper.utils import string_to_float


class NengunClient(ClientInterface):
    def get_parts(self):
        raise NotImplementedError

    async def get_part(self, reference):
        response, _, _ = await self.request_limiter.post(
            "https://2s2vpip9y6-dsn.algolia.net/1/indexes/*/queries?x-algolia-application-id=2S2VPIP9Y6&x-algolia-api-key=cfae1d1ea01383e7391675de61d0eb8b",
            data=json.dumps(
                {
                    "requests": [
                        {"indexName": "nengun_search", "params": f"query={reference}"}
                    ]
                }
            ),
        )

        for hit in response["results"][0]["hits"]:
            if hit["code"] == reference:
                response, _, _ = await self.request_limiter.get(hit["url"])
                soup = BeautifulSoup(response, "html.parser")
                return Stock(
                    reference=reference,
                    url=hit["url"],
                    source=SOURCE_NENGUN,
                    country="JP",
                    title=soup.find("meta", property="og:title")["content"],
                    price=Money(
                        round(
                            string_to_float(soup.find("div", {"class": "price"}).text),
                            2,
                        ),
                        "EUR",
                    ),
                    image=soup.find("meta", property="og:image")["content"],
                    available=True,
                )
