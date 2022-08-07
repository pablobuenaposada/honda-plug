from abc import ABC, abstractmethod


class ClientInterface(ABC):
    @abstractmethod
    def get_part(self, part_number):
        pass
