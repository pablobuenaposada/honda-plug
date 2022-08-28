from scrapper.clients.piecesautohonda import PiecesAutoHondaClient


def run():
    PiecesAutoHondaClient().get_parts()
