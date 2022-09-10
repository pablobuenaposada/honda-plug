import re
import time
from datetime import datetime

import aiohttp


class RequestLimiter:
    WAIT_SECONDS = 3

    def __init__(self):
        self.last_time = datetime.now()

    async def get(self, url, *, allow_redirects=True, **kwargs):
        delta = (datetime.now() - self.last_time).seconds
        if delta < self.WAIT_SECONDS:
            time.sleep(self.WAIT_SECONDS - delta)
        self.last_time = datetime.now()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, allow_redirects=allow_redirects, **kwargs
            ) as response:
                if response.content_type == "application/json":
                    return await response.json(), response.url, response.status
                elif response.content_type == "text/html":
                    return await response.text(), response.url, response.status


def string_to_float(value: str):
    return float(re.findall("\d+\.\d+", value)[0])


def format_reference(reference):
    return reference.strip().replace("-", "").upper()
