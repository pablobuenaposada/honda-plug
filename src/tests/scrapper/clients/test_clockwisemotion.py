import pytest
from scrapper.clients.clockwisemotion import ClockwiseMotionClient


@pytest.mark.django_db
@pytest.mark.skip()
class TestClockwiseMotionClient:
    def test_success(self):
        ClockwiseMotionClient().get_parts()
        pass
