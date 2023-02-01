from bs4 import BeautifulSoup
from money import Money
from part.constants import SOURCE_CMS
from scrapper.clients.interface import ClientInterface
from scrapper.common.stock import Stock
from scrapper.utils import flatten_reference, string_to_float


class CmsClient(ClientInterface):
    def get_parts(self):
        raise NotImplementedError

    async def get_part(self, reference):
        flat_ref = flatten_reference(reference)
        response, _, _ = await self.request_limiter.get(
            "https://www.cmsnl.com/search/ac.php",
            params={
                "q": flat_ref,
            },
        )

        if len(response) > 1:
            for result in response[1:]:
                if result["value"] == flat_ref:
                    url = BeautifulSoup(result["label"], "html.parser").a["href"]
                    response, _, _ = await self.request_limiter.get(url)
                    soup = BeautifulSoup(response, "html.parser").find(
                        "img", {"id": "product_imgmedium"}
                    )
                    image = (
                        soup["src"]
                        if soup["src"] != "https://images.cmsnl.com/404.jpg"
                        else None
                    )
                    soup = BeautifulSoup(response, "html.parser").find(
                        "div", {"class": "callout"}
                    )
                    title = soup.strong.text.strip()
                    if (
                        "Product is not available"
                        in soup.find("div", {"class": "callout warning"}).p.text
                    ):
                        available = False
                    else:
                        available = True
                    response, _, _ = await self.request_limiter.get(
                        "https://www.cmsnl.com/ajx_srv.php",
                        params={"action": "getproductprice", "partcode": flat_ref},
                    )
                    price = round(string_to_float(response["salesprice"]) * 1.21, 2)
                    return Stock(
                        country="NL",
                        source=SOURCE_CMS,
                        reference=reference,
                        price=Money(
                            amount=str(price),
                            currency="EUR",
                        ),
                        title=title,
                        url=url,
                        available=available,
                        image=image,
                    )
