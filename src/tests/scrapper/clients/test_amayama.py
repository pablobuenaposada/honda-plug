import pytest
from scrapper.clients.amayama import AmayamaClient


@pytest.mark.skip()
class TestAmayamaClient:
    def test_success(self):
        AmayamaClient().get_parts(lambda x: print(x))
