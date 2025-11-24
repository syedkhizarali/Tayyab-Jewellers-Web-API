# services/loyalty.py
from sqlalchemy.orm import Session

from backend.models import Order


def calculate_loyalty_tier(order_count: int, total_spent: float):
    if total_spent > 500000:
        return "platinum", 15.0  # 15% discount
    elif total_spent > 200000:
        return "gold", 10.0
    elif total_spent > 50000:
        return "silver", 5.0
    else:
        return "standard", 0.0


def apply_loyalty_discount(user_id: int, order_total: float, db: Session):
    user_orders = db.query(Order).filter(
        Order.user_id == user_id,
        Order.status == "completed"
    ).all()

    order_count = len(user_orders)
    total_spent = sum(order.total_price for order in user_orders)

    tier, discount_percent = calculate_loyalty_tier(order_count, total_spent)
    discount_amount = (order_total * discount_percent) / 100

    return {
        "tier": tier,
        "discount_percent": discount_percent,
        "discount_amount": discount_amount,
        "final_amount": order_total - discount_amount
    }