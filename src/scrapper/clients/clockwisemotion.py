from bs4 import BeautifulSoup
from money import Money
from price_parser import Price

from part.constants import SOURCE_CLOCKWISEMOTION
from part.lambdas import add_stock
from scrapper.clients.interface import ClientInterface
from scrapper.common.stock import Stock


class ClockwiseMotionClient(ClientInterface):
    def get_part(self, part_number):
        raise NotImplementedError

    def get_parts(self):
        for page in [{}, {"page": "1"}, {"page": "2"}]:
            response = self.request_limiter.get(
                "https://www.clockwisemotion.co.uk/products/search/manufacturer/honda-oem-72",
                params=page,
            )
            parts = BeautifulSoup(response.content, "html.parser").findAll(
                "div", {"class": "views-field views-field-field-images"}
            )

            for part in parts:
                response = self.request_limiter.get(part.a["href"])
                soup = BeautifulSoup(response.content, "html.parser")
                reference = (
                    soup.find("div", {"class": "commerce-product-sku-label"})
                    .next_sibling.strip()
                    .replace("Set", "")
                )
                title = soup.find(
                    "h2",
                    {
                        "class": "field field-name-title-field field-type-text field-label-above"
                    },
                ).text.strip()
                price = Price.fromstring(
                    soup.find("div", {"class": "price-inc-vat"}).text.strip()
                )
                quantity = int(
                    float(
                        soup.find(
                            "div",
                            {
                                "class": "field field-name-commerce-stock field-type-number-decimal field-label-above"
                            },
                        )
                        .select("div")[2]
                        .text.strip()
                    )
                )
                image = soup.find("a", {"class": "photoswipe"})["href"]
                available = bool(quantity)

                add_stock(
                    Stock(
                        reference=reference,
                        url=part.a["href"],
                        source=SOURCE_CLOCKWISEMOTION,
                        country="GB",
                        title=title,
                        price=Money(price.amount, "GBP"),
                        image=image,
                        available=available,
                        quantity=quantity,
                    ),
                    part.a["href"],
                )
