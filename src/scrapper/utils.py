import time
from datetime import datetime


class RequestLimiter:
    WAIT_SECONDS = 3

    def __init__(self, session):
        self.last_time = datetime.now()
        self.session = session

    def get(self, *args, **kwargs):
        delta = (datetime.now() - self.last_time).seconds
        if delta < self.WAIT_SECONDS:
            time.sleep(self.WAIT_SECONDS - delta)
        self.last_time = datetime.now()
        return self.session.get(*args, **kwargs)
