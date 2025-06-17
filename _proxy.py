# youtube_transcript_api/_proxy.py
from typing import List
import random


class GenericProxyConfig:
    """
    Proxy config that randomly chooses one of the given proxies.
    """

    def __init__(self, proxies: List[str]):
        self.proxies = proxies

    def get_proxy(self, url: str) -> str:
        return random.choice(self.proxies)
