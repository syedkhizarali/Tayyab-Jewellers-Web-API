from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import GoldRate
from backend.schemas import GoldRateOut, GoldRateCreate
from backend.utils.scraper import scrape_gold_prices
from backend.utils.calculation import price_per_gram_from_tola, karat_price_from_24k_tola
import time

router = APIRouter(prefix="/rates", tags=["rates"])

# Simple in-memory cache
_cache = {"value": None, "ts": 0}
CACHE_TTL = 60  # seconds


@router.get("/latest", response_model=list[GoldRateOut])
def latest_rates(db: Session = Depends(get_db)):

    # 1. Check cache
    if _cache["value"] and time.time() - _cache["ts"] < CACHE_TTL:
        return _cache["value"]

    # 2. Scrape live prices
    prices = scrape_gold_prices()   # FIXED NAME
    if not prices:
        # If scraping fails → fallback to DB
        rows = db.query(GoldRate).order_by(GoldRate.created_at.desc()).limit(6).all()
        if not rows:
            raise HTTPException(500, "No rate available")
        _cache["value"] = rows
        _cache["ts"] = time.time()
        return rows

    # 3. Build rate list using scraped data
    rates = []
    for karat in [24, 22, 21, 18, 12, 10]:

        # Convert from 24K price → selected karat
        tola_price = karat_price_from_24k_tola(prices, karat)  # FIXED

        gram_price = price_per_gram_from_tola(tola_price)

        gr = GoldRate(
            karat=karat,
            price_per_tola=tola_price,
            price_per_gram=gram_price,
            source="live"
        )
        db.add(gr)
        rates.append(gr)

    db.commit()

    # Update cache
    _cache["value"] = rates
    _cache["ts"] = time.time()

    return rates


@router.post("/manual", response_model=list[GoldRateOut])
def manual_insert(rate_in: GoldRateCreate, db: Session = Depends(get_db)):

    gram = price_per_gram_from_tola(rate_in.price_per_tola)

    obj = GoldRate(
        karat=rate_in.karat,
        price_per_tola=rate_in.price_per_tola,
        price_per_gram=gram,
        source=rate_in.source
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)

    return [obj]
