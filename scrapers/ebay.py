"""
DealScout – eBay Scraper
Scrapes eBay search results for deals.
DHD Data | Clients First. Perfection Always.
"""
import json
import re
from bs4 import BeautifulSoup
from .base import BaseScraper


class EbayScraper(BaseScraper):
    marketplace_name = "eBay"
    marketplace_id   = 1  # matches DB seed

    BASE = "https://www.ebay.com/sch/i.html"

    def search(self, keyword: str, max_price: float = None) -> list[dict]:
        params = {
            "_nkw":    keyword,
            "_sop":    "15",   # Best Match
            "LH_BIN":  "1",    # Buy It Now
            "_ipg":    "60",
        }
        if max_price:
            params["_udhi"] = str(max_price)

        deals = []
        try:
            resp = self._get(self.BASE, params=params)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "lxml")

            items = soup.select("li.s-item")
            for item in items:
                deal = self._parse_item(item)
                if deal:
                    deals.append(deal)
        except Exception as e:
            print(f"[eBay] Error: {e}")

        return deals

    def _parse_item(self, item) -> dict | None:
        try:
            title_el = item.select_one(".s-item__title")
            price_el = item.select_one(".s-item__price")
            url_el   = item.select_one("a.s-item__link")
            img_el   = item.select_one("img.s-item__image-img")
            loc_el   = item.select_one(".s-item__location")
            cond_el  = item.select_one(".SECONDARY_INFO")

            if not title_el or not price_el:
                return None

            title = title_el.get_text(strip=True)
            if title.lower() in ("shop on ebay", ""):
                return None

            price_text = price_el.get_text(strip=True)
            price = self._parse_price(price_text)

            deal = self._deal_template()
            deal.update({
                "title":     title,
                "price":     price,
                "url":       url_el["href"] if url_el else "",
                "image_url": img_el.get("src", "") if img_el else "",
                "location":  loc_el.get_text(strip=True).replace("From ", "") if loc_el else "",
                "condition": cond_el.get_text(strip=True) if cond_el else "Unknown",
                "raw_data":  json.dumps({"source": "ebay_search"}),
            })
            return deal
        except Exception:
            return None

    @staticmethod
    def _parse_price(text: str) -> float | None:
        text = text.replace(",", "")
        # Handle range "to" — take lower
        if " to " in text:
            text = text.split(" to ")[0]
        match = re.search(r"[\d.]+", text)
        return float(match.group()) if match else None
