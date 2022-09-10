import logging
import re

from bs4 import BeautifulSoup
from money import Money

from part.constants import SOURCE_PIECESAUTOHONDA
from scrapper.clients.interface import ClientInterface
from scrapper.common.stock import Stock
from scrapper.utils import format_reference

MAX_PAGE = 530500
logger = logging.getLogger(__name__)


class PiecesAutoHondaClient(ClientInterface):
    async def get_part(self, reference):
        raw_reference = format_reference(reference)
        url = f"https://www.pieces-auto-honda.fr/honda-voiture/affectation_pieces_detachees/{raw_reference}"
        response, _, _ = await self.request_limiter.get(url)
        soup = BeautifulSoup(response, "html.parser")

        if not soup.find("span", {"id": "ref_etiquette"}):
            # case where reference is not even found
            return
        if soup.body.find(text=re.compile("Référence de remplacement")):
            # discontinued case
            available = False
            discontinued = True
            price = None
        else:
            available = (
                False
                if soup.find("button", {"id": "bt_affiche_tarif"}) is None
                else True
            )
            discontinued = False
            price = (
                Money(
                    amount=soup.find("span", {"itemprop": "price"})["content"],
                    currency="EUR",
                )
                if available
                else None
            )

        return Stock(
            country="FR",
            source=SOURCE_PIECESAUTOHONDA,
            reference=reference,
            price=price,
            title=soup.find("div", {"class": "mt-4 mb-1 ms-3 ms-sm-0"}).text.strip(),
            url=url,
            available=available,
            discontinued=discontinued,
        )

    def get_parts(self):
        from part.lambdas import add_part

        base_url = "https://www.repuestos-honda.es"
        response = self.request_limiter.get(base_url)
        soup = BeautifulSoup(response.content, "html.parser")
        for model in soup.findAll("div", {"class": "col text-center height_150 mb-1"}):
            try:
                response = self.request_limiter.get(f'{base_url}{model.a["href"]}')
                for year in BeautifulSoup(response.content, "html.parser").findAll(
                    "div", {"class": "col text-center"}
                )[1:]:
                    response = self.request_limiter.get(f'{base_url}{year.a["href"]}')
                    for spec in BeautifulSoup(response.content, "html.parser").findAll(
                        "div", {"class": "col text-center"}
                    )[2:]:
                        response = self.request_limiter.get(
                            f'{base_url}{spec.a["href"]}'
                        )
                        for group in BeautifulSoup(
                            response.content, "html.parser"
                        ).findAll(
                            "div",
                            {
                                "class": "col-md-6 col-lg-4 infos_vehicle ps-2 align-self-center"
                            },
                        ):
                            response = self.request_limiter.get(
                                f'{base_url}{group.a["href"]}'
                            )
                            for inner_group in BeautifulSoup(
                                response.content, "html.parser"
                            ).findAll("div", {"class": "col p-1"}):
                                response = self.request_limiter.get(
                                    f'{base_url}{inner_group.a["href"]}'
                                )
                                for parts in BeautifulSoup(
                                    response.content, "html.parser"
                                ).findAll("span", {"class": "JS_ref_link"}):
                                    add_part(parts.text.strip(), SOURCE_PIECESAUTOHONDA)
            except Exception as error:
                logger.info(response.url)
                logger.info(error)
