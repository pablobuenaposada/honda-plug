import re

from bs4 import BeautifulSoup
from money import Money

from part.constants import SOURCE_PIECESAUTOHONDA
from scrapper.clients.interface import ClientInterface
from scrapper.common.stock import Stock
from scrapper.utils import format_reference


class PiecesAutoHondaClient(ClientInterface):
    def get_part(self, reference):
        raw_reference = format_reference(reference)
        url = f"https://www.pieces-auto-honda.fr/honda-voiture/affectation_pieces_detachees/{raw_reference}"
        response = self.request_limiter.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

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
        raise NotImplementedError
