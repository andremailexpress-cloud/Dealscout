"""
DealScout – Base Scraper
DHD Data | Clients First. Perfection Always.
"""
import requests
import random
import time
from abc import ABC, abstractmethod
from datetime import datetime

HEADERS_POOL = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0"},
]


class BaseScraper(ABC):
    """All marketplace scrapers inherit from this."""

    marketplace_name: str = "Unknown"
    marketplace_id:   int = None

    def __init__(self, timeout=15, delay=(1, 3)):
        self.timeout = timeout
        self.delay   = delay
        self.session = requests.Session()
        self.session.headers.update(random.choice(HEADERS_POOL))

    def _get(self, url: str, **kwargs) -> requests.Response:
        time.sleep(random.uniform(*self.delay))
        self.session.headers.update(random.choice(HEADERS_POOL))
        return self.session.get(url, timeout=self.timeout, **kwargs)

    @abstractmethod
    def search(self, keyword: str, max_price: float = None) -> list[dict]:
        """Return a list of deal dicts."""
        ...

    def _deal_template(self) -> dict:
        return {
            "marketplace_id":  self.marketplace_id,
            "category_id":     None,
            "title":           "",
            "description":     "",
            "price":           None,
            "original_price":  None,
            "currency":        "USD",
            "discount_pct":    None,
            "url":             "",
            "image_url":       "",
            "location":        "",
            "seller":          "",
            "condition":       "Unknown",
            "raw_data":        None,
        }
