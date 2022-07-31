import pytest

from part.lambdas import add_part
from scrapper.clients.epcdata import EpcdataClient


@pytest.mark.django_db
class TestEpcdataClient:
    def test_success(self):
        # EpcdataClient().get_parts(add_part)
        pass
