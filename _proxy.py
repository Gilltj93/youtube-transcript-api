# youtube_transcript_api/_proxy.py

import random

class GenericProxyConfig:
    def __init__(self, proxies, proxy_selection_method='random'):
        self.proxies = proxies
        self.proxy_selection_method = proxy_selection_method

    def get_proxy(self):
        if self.proxy_selection_method == 'random':
            return random.choice(self.proxies)
        elif self.proxy_selection_method == 'round_robin':
            proxy = self.proxies.pop(0)
            self.proxies.append(proxy)
            return proxy
        else:
            raise ValueError("Invalid proxy selection method.")
