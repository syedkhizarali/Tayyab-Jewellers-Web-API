from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import GoldRate
from backend.schemas import GoldRateOut, GoldRateCreate
from backend.utils.scraper import scrape_24k_tola_from_goldrateupdate
from backend.utils.calculation import price_per_gram_from_tola, karat_price_from_24k_tola
import time

router = APIRouter(prefix="/rates", tags=["rates"])

_cache = {"value": None, "ts": 0}
CACHE_TTL = 60  # seconds

@router.get("/latest", response_model=list[GoldRateOut])
def latest_rates(db: Session = Depends(get_db)):
    if _cache["value"] and time.time() - _cache["ts"] < CACHE_TTL:
        return _cache["value"]

    tola_24k = scrape_24k_tola_from_goldrateupdate()
    if not tola_24k:
        rows = db.query(GoldRate).order_by(GoldRate.created_at.desc()).limit(6).all()
        if not rows:
            raise HTTPException(500, "No rate available")
        _cache["value"] = rows
        _cache["ts"] = time.time()
        return rows

    rates = []
    for karat in [24,22,21,18,12,10]:
        tola = karat_price_from_24k_tola(tola_24k, karat)
        gram = price_per_gram_from_tola(tola)
        gr = GoldRate(karat=karat, price_per_tola=tola, price_per_gram=gram, source="live")
        db.add(gr)
        rates.append(gr)
    db.commit()
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
