from scrapper.clients.clockwisemotion import ClockwiseMotionClient


def run(*args):
    ClockwiseMotionClient().get_parts()
