from datetime import datetime, timedelta

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database import get_db
from backend.models import Order, OrderItem, Product, Payment
from backend.routes.admin import router
from backend.security import require_admin


def generate_sales_report(db: Session, since_days: int = 30):
    date_from = datetime.utcnow() - timedelta(days=since_days)

    # Total orders
    total_orders = db.query(func.count(Order.id)) \
        .filter(Order.created_at >= date_from).scalar()

    # Total revenue from payments
    total_revenue = db.query(func.sum(Payment.amount)) \
        .filter(Payment.created_at >= date_from).scalar() or 0

    # Top 5 best-selling products
    top_products = (
        db.query(Product.name, func.sum(OrderItem.quantity).label("qty"))
        .join(OrderItem, Product.id == OrderItem.product_id)
        .join(Order, Order.id == OrderItem.order_id)
        .filter(Order.created_at >= date_from)
        .group_by(Product.id)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(5)
        .all()
    )

    return {
        "since_days": since_days,
        "total_orders": total_orders,
        "total_revenue": float(total_revenue),
        "top_products": [{"name": p[0], "sold_qty": p[1]} for p in top_products]
    }


@router.get("/analytics/sales")
def get_sales_analytics(
        start_date: datetime,
        end_date: datetime,
        db: Session = Depends(get_db),
        admin=Depends(require_admin)
):
    # Sales by period
    sales_data = db.query(Order).filter(
        Order.placed_at.between(start_date, end_date),
        Order.status == "completed"
    ).all()

    total_revenue = sum(order.total_price for order in sales_data)
    orders_count = len(sales_data)

    return {
        "period": f"{start_date} to {end_date}",
        "total_revenue": total_revenue,
        "orders_count": orders_count,
        "average_order_value": total_revenue / orders_count if orders_count else 0
    }