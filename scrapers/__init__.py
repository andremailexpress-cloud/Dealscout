"""DealScout Scrapers Package"""
from .base import BaseScraper
from .ebay import EbayScraper
from .gumtree import GumtreeScraper
from .craigslist import CraigslistScraper

SCRAPERS = {
    "eBay":      EbayScraper,
    "Gumtree":   GumtreeScraper,
    "Craigslist": CraigslistScraper,
}
