from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Order, User, OrderItem, Product
from backend.security import require_admin
from datetime import date

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/dashboard")
def admin_dashboard(admin=Depends(require_admin), db: Session = Depends(get_db)):
    total_orders = db.query(func.count(Order.id)).scalar() or 0
    total_customers = db.query(func.count(User.id)).scalar() or 0
    total_revenue = db.query(func.coalesce(func.sum(Order.total_price), 0.0)).scalar() or 0.0
    today = date.today()
    todays_orders = db.query(func.count(Order.id)).filter(func.date(Order.placed_at) == today).scalar() or 0

    best = (
        db.query(Product.name, func.coalesce(func.sum(OrderItem.quantity), 0).label("sold"))
        .join(OrderItem, Product.id == OrderItem.product_id)
        .group_by(Product.id)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(5)
        .all()
    )

    best_products = [{"name": r[0], "sold": int(r[1])} for r in best]
    return {
        "total_orders": int(total_orders),
        "total_customers": int(total_customers),
        "total_revenue": float(total_revenue),
        "todays_orders": int(todays_orders),
        "best_products": best_products
    }
