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

    async def post(self, url, *, data=None, **kwargs):
        delta = (datetime.now() - self.last_time).seconds
        if delta < self.WAIT_SECONDS:
            time.sleep(self.WAIT_SECONDS - delta)
        self.last_time = datetime.now()
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, **kwargs) as response:
                return await response.json(), response.url, response.status


def string_to_float(value: str):
    return float(re.findall("\d+\.\d+", value)[0])


def flatten_reference(reference):
    return reference.strip().replace("-", "").upper()


def format_reference(reference):
    reference = flatten_reference(reference)
    if len(reference) == 10:
        return f"{reference[:5]}-{reference[5:]}"
    if 10 <= len(reference) <= 11:
        if reference[5:8].isdigit():
            return f"{reference[:5]}-{reference[5:]}"
        else:
            return f"{reference[:5]}-{reference[5:8]}-{reference[8:]}"
    if 12 <= len(reference) <= 13:
        return f"{reference[:5]}-{reference[5:8]}-{reference[8:]}"
