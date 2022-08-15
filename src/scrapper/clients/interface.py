from abc import ABC, abstractmethod

from scrapper.utils import RequestLimiter


class ClientInterface(ABC):
    def __init__(self):
        self.request_limiter = RequestLimiter()

    @abstractmethod
    def get_part(self, reference):
        pass

    @abstractmethod
    def get_parts(self):
        pass
