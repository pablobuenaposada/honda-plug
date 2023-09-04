import json

from money import Money
from part.constants import SOURCE_ALL4HONDA
from price_parser import Price
from scrapper.clients.interface import ClientInterface
from scrapper.common.stock import Stock


class All4hondaClient(ClientInterface):
    def get_parts(self):
        raise NotImplementedError

    async def get_part(self, reference):
        response, _, _ = await self.request_limiter.post(
            "https://nnvjvcwb78-dsn.algolia.net/1/indexes/magento2_en_products/query?x-algolia-application-id=NNVJVCWB78&x-algolia-api-key=YmM2ZWQ3MGQwMjI2OGJiNjI2ZDdlYjQzZTM0ZjBiNDlhNTQzYzk4ZDhkMWExYWJjNGU0YzMwYWVjY2U1YjJkOXRhZ0ZpbHRlcnM9",
            data=json.dumps({"params": f"query={reference}"}),
        )
        formatted_referenced = reference.upper().replace("-", "")

        for hit in response["hits"]:
            if isinstance(hit["sku"], list):
                for sku in hit["sku"]:
                    if sku.upper().replace("-", "") == formatted_referenced:
                        return Stock(
                            country="NL",
                            reference=reference,
                            url=hit["url"],
                            source=SOURCE_ALL4HONDA,
                            title=hit["name"],
                            price=Money(hit["price"]["EUR"]["default"], "EUR"),
                            image=f'https://{hit["image_url"][2:]}',
                        )
            else:
                if hit["sku"].upper().replace("-", "") == formatted_referenced:
                    price = Price.fromstring(hit["price"]["EUR"]["default_formated"])
                    return Stock(
                        country="NL",
                        reference=reference,
                        url=hit["url"],
                        source=SOURCE_ALL4HONDA,
                        title=hit["name"],
                        price=Money(price.amount, "EUR"),
                        image=f'https://{hit["image_url"][2:]}',
                    )
