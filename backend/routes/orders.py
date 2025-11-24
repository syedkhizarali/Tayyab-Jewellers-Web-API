import asyncio

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, logger
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Order, OrderItem, Product, User
from backend.schemas import OrderCreate, OrderOut
from backend.security import require_admin
from backend.services.email_services import send_email_smtp, send_order_status_email
from backend.utils.discount import calculate_loyalty_discount

router = APIRouter(prefix="/orders", tags=["orders"])
LOW_STOCK_THRESHOLD = 2

@router.post("/", response_model=OrderOut)
def create_order(order_in: OrderCreate, background: BackgroundTasks, db: Session = Depends(get_db)):
    total_price = 0
    order_items = []
    user = db.query(User).filter(User.id == order_in.user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    for item in order_in.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(404, f"Product {item.product_id} not found")
        if product.stock_quantity < item.quantity:
            raise HTTPException(400, f"Not enough stock for product {product.name}")

        unit_price = product.price + product.making_charge
        total = unit_price * item.quantity
        total_price += total
        order_items.append(OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=unit_price,
            total_price=total
        ))

        # decrement stock
        product.stock_quantity -= item.quantity
        if product.stock_quantity <= LOW_STOCK_THRESHOLD:
            # notify admin in background
            background.add_task(send_email_smtp,
                                to_email="admin@tayyab.com",
                                subject="Low stock alert",
                                body=f"Product {product.name} low: {product.stock_quantity} left.")

    # apply simple loyalty discount if any (optional)
    # order_count = db.query(Order).filter(Order.user_id == user.id).count()
    # discount_percent = calculate_loyalty_discount(order_count)
    # if discount_percent:
    #     total_price = total_price * (1 - discount_percent/100)

    order = Order(
        user_id=order_in.user_id,
        delivery_address=order_in.delivery_address,
        delivery_region=order_in.delivery_region,
        total_price=total_price,
        items=order_items
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # send order confirmation email in background
    background.add_task(send_email_smtp, user.email, "Order Confirmed", f"Your order #{order.id} is received. Total: {order.total_price}")

    return order
    with log_exceptions("Create order"):
        # your existing order creation logic
        pass


@router.put("/orders/{order_id}/status")
def update_order_status(
        order_id: int,
        new_status: str,
        db: Session = Depends(get_db),
        admin=Depends(require_admin)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(404, "Order not found")

    old_status = order.status
    order.status = new_status
    db.commit()

    # Send notification
    user_email = order.user.email
    asyncio.create_task(send_order_status_email(user_email, order_id, new_status))

    logger.info(f"Order {order_id} status changed: {old_status} -> {new_status}")
    return order
