"""
DealScout – Craigslist Scraper
DHD Data | Clients First. Perfection Always.
"""
import json
import re
from bs4 import BeautifulSoup
from .base import BaseScraper


class CraigslistScraper(BaseScraper):
    marketplace_name = "Craigslist"
    marketplace_id   = 4

    # Searches across all cities via the main search endpoint
    BASE = "https://www.craigslist.org/search/sss"

    def search(self, keyword: str, max_price: float = None) -> list[dict]:
        params = {"query": keyword, "sort": "date"}
        if max_price:
            params["max_price"] = str(int(max_price))

        deals = []
        try:
            resp = self._get(self.BASE, params=params)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "lxml")
            items = soup.select("li.cl-search-result")
            for item in items:
                deal = self._parse_item(item)
                if deal:
                    deals.append(deal)
        except Exception as e:
            print(f"[Craigslist] Error: {e}")

        return deals

    def _parse_item(self, item) -> dict | None:
        try:
            title_el = item.select_one("a.cl-app-anchor .label")
            link_el  = item.select_one("a.cl-app-anchor")
            price_el = item.select_one(".priceinfo")
            loc_el   = item.select_one(".meta .separator + span") or item.select_one(".location")

            if not title_el:
                return None

            price = self._parse_price(price_el.get_text(strip=True)) if price_el else None

            deal = self._deal_template()
            deal.update({
                "title":    title_el.get_text(strip=True),
                "price":    price,
                "url":      link_el["href"] if link_el else "",
                "location": loc_el.get_text(strip=True) if loc_el else "",
                "raw_data": json.dumps({"source": "craigslist_search"}),
            })
            return deal
        except Exception:
            return None

    @staticmethod
    def _parse_price(text: str) -> float | None:
        text = text.replace(",", "")
        match = re.search(r"[\d.]+", text)
        return float(match.group()) if match else None
