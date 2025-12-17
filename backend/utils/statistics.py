import matplotlib.pyplot as plt
from backend.database import SessionLocal
from backend.models import GoldRateHistory
import io

def generate_gold_history_chart():
    db = SessionLocal()
    records = db.query(GoldRateHistory).order_by(GoldRateHistory.year.asc()).all()
    db.close()

    years = [r.year for r in records]
    prices = [r.avg_price_per_tola for r in records]

    plt.figure(figsize=(7,4))
    plt.plot(years, prices, marker="o", linestyle="-", linewidth=2)
    plt.title("Gold Rate (Last 5 Years)")
    plt.xlabel("Year")
    plt.ylabel("Avg Price per Tola (PKR)")
    plt.grid(True)

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    return buffer
