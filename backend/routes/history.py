# Enhanced routes/history.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import GoldRateHistory, GoldAnalysisPost, GoldRate
from backend.schemas import GoldHistoryIn, GoldAnalysisCreate, GoldAnalysisOut
from typing import List

from backend.security import require_admin

router = APIRouter(prefix="/history", tags=["gold-history"])


# --- Gold Rate History Tracking ---
@router.post("/gold-rates", response_model=GoldHistoryIn)
def add_gold_rate_history(history_in: GoldHistoryIn, db: Session = Depends(get_db)):
    """Add historical gold rate data (for charts/analysis)"""
    history = GoldRateHistory(**history_in.dict())
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


@router.get("/gold-rates/{year}")
def get_gold_rates_by_year(year: int, db: Session = Depends(get_db)):
    """Get gold rates for a specific year with trend analysis"""
    rates = db.query(GoldRateHistory).filter(GoldRateHistory.year == year).all()

    if not rates:
        raise HTTPException(404, f"No data for year {year}")

    # Calculate trends
    prices = [r.avg_price_per_tola for r in rates]
    avg_price = sum(prices) / len(prices)
    max_price = max(prices)
    min_price = min(prices)
    trend = "bullish" if prices[-1] > prices[0] else "bearish"

    return {
        "year": year,
        "records": rates,
        "analysis": {
            "average_price": avg_price,
            "highest_price": max_price,
            "lowest_price": min_price,
            "market_trend": trend,
            "price_change_percentage": ((prices[-1] - prices[0]) / prices[0]) * 100
        }
    }


# --- Gold Market Analysis Blog Posts ---
@router.post("/analysis", response_model=GoldAnalysisOut)
def create_gold_analysis(
        analysis_in: GoldAnalysisCreate,
        db: Session = Depends(get_db),
        admin=Depends(require_admin)
):
    """Create gold market analysis blog posts"""
    analysis = GoldAnalysisPost(**analysis_in.dict())
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


@router.get("/analysis", response_model=List[GoldAnalysisOut])
def get_gold_analysis_posts(
        limit: int = 10,
        db: Session = Depends(get_db)
):
    """Get gold market analysis blog posts"""
    posts = db.query(GoldAnalysisPost).order_by(GoldAnalysisPost.created_at.desc()).limit(limit).all()
    return posts


@router.get("/analysis/trends")
def get_current_gold_trends(db: Session = Depends(get_db)):
    """Get current gold market trends analysis"""
    # Analyze recent gold rates for trends
    recent_rates = db.query(GoldRate).order_by(GoldRate.created_at.desc()).limit(30).all()

    if len(recent_rates) < 2:
        return {"trend": "neutral", "message": "Insufficient data for trend analysis"}

    recent_prices = [r.price_per_tola for r in recent_rates]
    week_avg = sum(recent_prices[:7]) / 7
    month_avg = sum(recent_prices) / len(recent_prices)

    current_price = recent_prices[0]
    trend = "bullish" if current_price > month_avg else "bearish"
    volatility = (max(recent_prices) - min(recent_prices)) / month_avg * 100

    return {
        "current_price": current_price,
        "trend": trend,
        "weekly_average": week_avg,
        "monthly_average": month_avg,
        "volatility_percentage": round(volatility, 2),
        "recommendation": "Buy" if trend == "bullish" else "Hold" if volatility < 5 else "Wait"
    }
def get_investment_advice(overall_change: float, recent_change: float) -> str:
    """Generate investment advice based on gold trends"""
    if overall_change > 20 and recent_change > 5:
        return "Strong bullish trend - Good time to invest"
    elif overall_change > 10 and recent_change > 0:
        return "Moderate growth - Consider investing"
    elif overall_change < -10:
        return "Market downturn - Good buying opportunity"
    else:
        return "Market stable - Good time for long-term investment"