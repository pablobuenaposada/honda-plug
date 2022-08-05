import logging

import requests
from bs4 import BeautifulSoup
from django.db.utils import IntegrityError

from part.constants import SOURCE_AMAYAMA
from scrapper.utils import RequestLimiter


class AmayamaClient:
    logger = logging.getLogger(__name__)
    DOMAIN = "amayama.com"

    def get_parts(self, function):
        session = requests.Session()
        request_limiter = RequestLimiter(session)
        response = request_limiter.get(f"https://{self.DOMAIN}/en/catalogs/honda")

        models = BeautifulSoup(response.content, "html.parser").findAll(
            "a", {"class": "list-group-item"}
        )
        for model in models:
            response = request_limiter.get(model["href"])
            generations = (
                BeautifulSoup(response.content, "html.parser")
                .findAll("div", {"class": "list"})[0]
                .findAll("a")
            )

            for generation in generations:
                response = request_limiter.get(
                    f'https://{self.DOMAIN}{generation["href"]}'
                )
                part_groups = (
                    BeautifulSoup(response.content, "html.parser")
                    .findAll("div", {"class": "list"})[0]
                    .findAll("a")
                )

                for part_group in part_groups:
                    response = request_limiter.get(
                        f'https://{self.DOMAIN}{part_group["href"]}'
                    )
                    schemas_list = BeautifulSoup(
                        response.content, "html.parser"
                    ).findAll("div", {"class": "schemas-list-item"})

                    for schema in schemas_list:
                        response = request_limiter.get(
                            f'https://{self.DOMAIN}{schema.a["href"]}'
                        )
                        parts = BeautifulSoup(response.content, "html.parser").findAll(
                            "tr", {"class": "map-item link"}
                        )

                        for part in parts:
                            try:
                                self.logger.info(f"found {part.a.text}")
                                function(part.a.text, SOURCE_AMAYAMA)
                            except IntegrityError:
                                self.logger.info("already in")
                            except Exception as e:
                                self.logger.info(e)
                            else:
                                self.logger.info(f"added")
