import logging
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from django.db.utils import IntegrityError


class RequestLimiter:
    WAIT_SECONDS = 3

    def __init__(self, session):
        self.last_time = datetime.now()
        self.session = session

    def get(self, *args, **kwargs):
        delta = (datetime.now() - self.last_time).seconds
        if delta < self.WAIT_SECONDS:
            time.sleep(self.WAIT_SECONDS - delta)
        self.last_time = datetime.now()
        return self.session.get(*args, **kwargs)


class EpcdataClient:
    logger = logging.getLogger(__name__)
    DOMAIN = "honda.epc-data.com"

    def get_parts(self, function):
        self.logger.info("START")
        session = requests.Session()
        request_limiter = RequestLimiter(session)
        response = request_limiter.get(f"https://{self.DOMAIN}")

        soup = BeautifulSoup(response.content, "html.parser").findAll(
            "ul", {"class": "category2"}
        )
        model_urls = [f'https://{self.DOMAIN}{model.a["href"]}' for model in soup]

        for model_url in model_urls:
            response = request_limiter.get(model_url)
            soup = BeautifulSoup(response.content, "html.parser").findAll(
                "ul", {"class": "category2"}
            )
            chassis_urls = [
                f'https://{self.DOMAIN}{chassis.a["href"]}' for chassis in soup
            ]

            for chassis_url in chassis_urls:
                response = request_limiter.get(chassis_url)
                soup = BeautifulSoup(response.content, "html.parser").findAll(
                    nowrap="nowrap"
                )
                complectation_urls = [
                    f'https://{self.DOMAIN}{complectation.a["href"]}'
                    for complectation in soup
                ]

                for complectation_url in complectation_urls:
                    response = request_limiter.get(complectation_url)
                    soup = BeautifulSoup(response.content, "html.parser").findAll(
                        "table", {"class": "top_cars"}
                    )
                    group_urls = [
                        f'https://{self.DOMAIN}{group["href"]}'
                        for group in soup[1].findAll("a")
                    ]

                    for group_url in group_urls:
                        response = request_limiter.get(group_url)
                        soup = BeautifulSoup(response.content, "html.parser").findAll(
                            "a", {"style": "text-decoration:none;"}
                        )
                        sub_group_urls = [
                            f'https://{self.DOMAIN}{sub_group["href"]}'
                            for sub_group in soup
                        ]

                        for sub_group_url in sub_group_urls:
                            response = request_limiter.get(sub_group_url)
                            soup = BeautifulSoup(
                                response.content, "html.parser"
                            ).findAll("area")
                            parts_urls = [
                                f'https://{self.DOMAIN}{part["href"]}' for part in soup
                            ]

                            for parts_url in parts_urls:
                                response = request_limiter.get(parts_url)
                                soup = BeautifulSoup(
                                    response.content, "html.parser"
                                ).find("b", {"class": "parts-in-stock-widget_part-oem"})
                                try:
                                    self.logger.info(f"found {soup.text}")
                                    function(soup.text, "epc-data")
                                except IntegrityError:
                                    self.logger.info("already in")
                                except Exception as e:
                                    self.logger.info(e)
