import logging

import requests
from bs4 import BeautifulSoup

from part.constants import SOURCE_AMAYAMA
from scrapper.utils import RequestLimiter

DOMAIN = "amayama.com"


class AmayamaClient:
    def get_parts(self, function, start_from_model=None):
        session = requests.Session()
        request_limiter = RequestLimiter(session)
        response = request_limiter.get(f"https://{DOMAIN}/en/catalogs/honda")

        models = [
            tag_a["href"]
            for tag_a in BeautifulSoup(response.content, "html.parser").findAll(
                "a", {"class": "list-group-item"}
            )
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
                            function(part.a.text, SOURCE_AMAYAMA)
