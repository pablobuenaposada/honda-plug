from abc import ABC, abstractmethod

import requests

from scrapper.utils import RequestLimiter


class ClientInterface(ABC):
    def __init__(self):
        session = requests.Session()
        self.request_limiter = RequestLimiter(session)

    @abstractmethod
    def get_part(self, part_number):
        pass

    @abstractmethod
    def get_parts(self):
        pass
