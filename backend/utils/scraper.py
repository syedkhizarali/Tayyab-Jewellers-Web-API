import requests
from bs4 import BeautifulSoup
from backend.configs import settings

def scrape_gold_prices() -> dict[str, float] | None:
    """
    Scrape gold prices (24K, 22K, 21K, 18K) per tola from the GOLD_SCRAPER_URL.
    Returns a dictionary with karat as key and price as float.
    Example: {"24K": 215000.0, "22K": 198000.0, ...}
    Returns None if scraping fails.
    """
    try:
        url = settings.GOLD_SCRAPER_URL
        res = requests.get(url, timeout=10)
        res.raise_for_status()  # Raise exception for bad responses
        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text()

        gold_prices = {}
        for karat in ["24K", "22K", "21K", "18K"]:
            try:
                # Find the first number after the karat
                price_str = text.split(karat)[1].split()[0].replace(",", "")
                gold_prices[karat] = float(price_str)
            except (IndexError, ValueError):
                gold_prices[karat] = None  # Price not found

        return gold_prices

    except Exception as e:
        print("Scraping failed:", e)
        return None
