import re
import time
from datetime import datetime

import requests


class RequestLimiter:
    WAIT_SECONDS = 3

    def __init__(self):
        self.session = requests.Session()
        self.last_time = datetime.now()

    def get(self, *args, **kwargs):
        delta = (datetime.now() - self.last_time).seconds
        if delta < self.WAIT_SECONDS:
            time.sleep(self.WAIT_SECONDS - delta)
        self.last_time = datetime.now()
        try:
            return self.session.get(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            self.__init__()
            self.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        delta = (datetime.now() - self.last_time).seconds
        if delta < self.WAIT_SECONDS:
            time.sleep(self.WAIT_SECONDS - delta)
        self.last_time = datetime.now()
        try:
            return self.session.post(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            self.__init__()
            self.get(*args, **kwargs)


def string_to_float(value: str):
    return float(re.findall("\d+\.\d+", value)[0])


def format_reference(reference):
    return reference.strip().replace("-", "").upper()
