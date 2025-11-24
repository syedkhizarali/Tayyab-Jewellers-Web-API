import requests
from bs4 import BeautifulSoup
from app.configs import settings

def scrape_24k_tola_from_goldrateupdate() -> float | None:
    """
    Scrape 24K gold price per tola from the GOLD_SCRAPER_URL.
    Returns float if successful, None if fails.
    """
    try:
        url = settings.GOLD_SCRAPER_URL
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        # Example: Find table or span containing 24K gold price
        text = soup.get_text()
        price_str = text.split("24K")[1].split()[0].replace(",", "")
        return float(price_str)
    except Exception as e:
        print("Scraping failed:", e)
        return None
