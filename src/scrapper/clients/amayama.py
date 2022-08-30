import re

import pycountry
import requests
from bs4 import BeautifulSoup
from money import Money

from part.constants import SOURCE_AMAYAMA
from scrapper.clients.interface import ClientInterface
from scrapper.common.stock import Stock
from scrapper.utils import RequestLimiter, format_reference

DOMAIN = "amayama.com"


class AmayamaClient(ClientInterface):
    regex = re.compile("[^a-zA-Z]")

    def get_part(self, reference):
        stocks = []
        response = self.request_limiter.get(
            f"https://{DOMAIN}/en/part/honda/{format_reference(reference)}"
        )
        soup = BeautifulSoup(response.content, "html.parser")

        if "Permanently out of stock" in soup.text:
            return

        title = soup.find("div", {"class": "part-page__name"}).h1.text
        image = soup.find("figure", {"data-type": "photo-container"}).a["href"]
        for stock in soup.find("tbody", {"class": "part-table__body"}).findAll(
            "tr", {"class": lambda L: L and L.startswith("part-table__row")}
        ):
            country = self.regex.sub(
                "", stock.find("span", {"class": "warehouse-name"}).text
            )
            country = (
                "AE" if country == "UAE" else country
            )  # special case for Arab Emirates
            country = pycountry.countries.search_fuzzy(country)[0]
            price = stock.find("span", {"class": "part-price"}).text.replace(",", "")
            try:
                quantity = int(stock.find("span", {"class": "part-quantity"}).text)
                available = True
            except ValueError:
                quantity = None
                available = None

            stocks.append(
                Stock(
                    country=country.alpha_2,
                    source=SOURCE_AMAYAMA,
                    reference=reference,
                    price=Money(price, "USD"),
                    title=title,
                    url=response.url,
                    quantity=quantity,
                    image=image,
                    available=available,
                )
            )
        return stocks

    def get_parts(self, function, start_from_model=None):
        from part.lambdas import add_stock

        session = requests.Session()
        request_limiter = RequestLimiter(session)
        response = request_limiter.get(f"https://{DOMAIN}/en/catalogs/honda")

        models = [
            tag_a["href"]
            for tag_a in BeautifulSoup(response.content, "html.parser").findAll(
                "a", {"class": "list-group-item"}
            )
            if "genuine-catalogs"
            not in tag_a["href"]  # filter out some models that gives problems
        ]
        if start_from_model:
            models = models[models.index(start_from_model) :]

        for model in models:
            response = request_limiter.get(model)
            generations = (
                BeautifulSoup(response.content, "html.parser")
                .findAll("div", {"class": "list"})[0]
                .findAll("a")
            )

            for generation in generations:
                response = request_limiter.get(f'https://{DOMAIN}{generation["href"]}')
                part_groups = (
                    BeautifulSoup(response.content, "html.parser")
                    .findAll("div", {"class": "list"})[0]
                    .findAll("a")
                )

                for part_group in part_groups:
                    response = request_limiter.get(
                        f'https://{DOMAIN}{part_group["href"]}'
                    )
                    schemas_list = BeautifulSoup(
                        response.content, "html.parser"
                    ).findAll("div", {"class": "schemas-list-item"})

                    for schema in schemas_list:
                        response = request_limiter.get(
                            f'https://{DOMAIN}{schema.a["href"]}'
                        )
                        parts = BeautifulSoup(response.content, "html.parser").findAll(
                            "tr", {"class": "map-item link"}
                        )

                        for part in parts:
                            reference = part.a.text
                            response = request_limiter.get(
                                f'https://{DOMAIN}{part.a["href"]}'
                            )
                            soup = BeautifulSoup(response.content, "html.parser")
                            title = soup.find(
                                "div", {"class": "part-page__name"}
                            ).h1.text
                            url = f'https://{DOMAIN}{part.a["href"]}'
                            stocks = soup.find(
                                "tbody", {"class": "part-table__body"}
                            ).findAll(
                                "tr",
                                {
                                    "class": lambda L: L
                                    and L.startswith("part-table__row")
                                },
                            )

                            for stock in stocks:
                                country = stock.find(
                                    "span", {"class": "warehouse-name"}
                                ).text
                                country = self.regex.sub("", country)
                                country = (
                                    "AE" if country == "UAE" else country
                                )  # special case for Arab Emirates
                                country = pycountry.countries.search_fuzzy(country)[0]
                                price = stock.find(
                                    "span", {"class": "part-price"}
                                ).text.replace(",", "")
                                quantity = stock.find(
                                    "span", {"class": "part-quantity"}
                                ).text
                                add_stock(
                                    Stock(
                                        reference=reference,
                                        url=url,
                                        source=SOURCE_AMAYAMA,
                                        country=country.alpha_2,
                                        title=title,
                                        price=Money(price, "USD"),
                                    ),
                                    model,
                                )
