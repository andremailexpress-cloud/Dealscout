"""
DealScout – Gumtree Scraper
DHD Data | Clients First. Perfection Always.
"""
import json
import re
from bs4 import BeautifulSoup
from .base import BaseScraper


class GumtreeScraper(BaseScraper):
    marketplace_name = "Gumtree"
    marketplace_id   = 3

    BASE = "https://www.gumtree.com/search"

    def search(self, keyword: str, max_price: float = None) -> list[dict]:
        params = {
            "search_query":    keyword,
            "search_location": "UK Wide",
            "search_category": "all",
            "TrAdBooked":      "false",
        }
        if max_price:
            params["max_price"] = str(int(max_price))

        deals = []
        try:
            resp = self._get(self.BASE, params=params)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "lxml")
            items = soup.select("article.listing-maxi")
            for item in items:
                deal = self._parse_item(item)
                if deal:
                    deals.append(deal)
        except Exception as e:
            print(f"[Gumtree] Error: {e}")

        return deals

    def _parse_item(self, item) -> dict | None:
        try:
            title_el = item.select_one("h2.listing-title a")
            price_el = item.select_one(".listing-price strong")
            desc_el  = item.select_one(".listing-description p")
            loc_el   = item.select_one(".listing-location span")
            img_el   = item.select_one("img")

            if not title_el:
                return None

            price_text = price_el.get_text(strip=True) if price_el else "0"
            price = self._parse_price(price_text)

            deal = self._deal_template()
            deal.update({
                "title":       title_el.get_text(strip=True),
                "description": desc_el.get_text(strip=True) if desc_el else "",
                "price":       price,
                "currency":    "GBP",
                "url":         "https://www.gumtree.com" + title_el["href"] if title_el.get("href","").startswith("/") else title_el.get("href",""),
                "image_url":   img_el.get("src","") if img_el else "",
                "location":    loc_el.get_text(strip=True) if loc_el else "",
                "raw_data":    json.dumps({"source": "gumtree_search"}),
            })
            return deal
        except Exception:
            return None

    @staticmethod
    def _parse_price(text: str) -> float | None:
        text = text.replace(",", "").replace("£", "").replace("$", "")
        match = re.search(r"[\d.]+", text)
        return float(match.group()) if match else None
