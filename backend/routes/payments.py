from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Payment, Order
from backend.schemas import PaymentMethod, PaymentStatus, PaymentCreate, PaymentOut
from datetime import datetime

router = APIRouter(prefix="/payments", tags=["payments"])

# Bank configurations for Pakistan
PAKISTAN_BANKS = {
    "hbl": "Habib Bank Limited",
    "ubl": "United Bank Limited",
    "mcb": "Muslim Commercial Bank",
    "abl": "Allied Bank Limited",
    "bank_alfalah": "Bank Alfalah",
    "meezan": "Meezan Bank"
}

@router.post("/", response_model=PaymentOut)
def make_payment(payment_in: PaymentCreate, db: Session = Depends(get_db)):
    # Validate order exists and get order details
    order = db.query(Order).filter(Order.id == payment_in.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Validate amount matches order total
    if payment_in.amount != order.total_price:  # Fixed: total_amount -> total_price
        raise HTTPException(status_code=400, detail="Payment amount doesn't match order total")

    # Process payment based on method
    if payment_in.method == PaymentMethod.BANK_TRANSFER:
        return process_bank_transfer(payment_in, order, db)
    elif payment_in.method in [PaymentMethod.JAZZ_CASH, PaymentMethod.EASYPAISA]:
        return process_mobile_wallet(payment_in, order, db)
    elif payment_in.method in [PaymentMethod.STRIPE, PaymentMethod.PAYPAL]:
        return process_international_payment(payment_in, order, db)
    else:
        raise HTTPException(status_code=400, detail="Unsupported payment method")

def process_bank_transfer(payment_in: PaymentCreate, order: Order, db: Session):
    """Process bank transfer payment"""
    if not payment_in.bank_name or not payment_in.transaction_id:
        raise HTTPException(status_code=400, detail="Bank name and transaction ID required for bank transfers")

    # Validate bank
    if payment_in.bank_name not in PAKISTAN_BANKS.values():
        raise HTTPException(status_code=400, detail="Unsupported bank")

    # Create payment record with pending status
    payment = Payment(
        order_id=payment_in.order_id,
        method=PaymentMethod.BANK_TRANSFER,
        amount=payment_in.amount,
        currency=payment_in.currency,
        status=PaymentStatus.PENDING,  # Wait for manual verification
        bank_name=payment_in.bank_name,
        transaction_id=payment_in.transaction_id,
        transaction_date=datetime.utcnow()
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment

def process_mobile_wallet(payment_in: PaymentCreate, order: Order, db: Session):
    """Process JazzCash or EasyPaisa payment"""
    payment = Payment(
        order_id=payment_in.order_id,
        method=payment_in.method,
        amount=payment_in.amount,
        currency="PKR",
        status=PaymentStatus.PAID,  # Assuming instant verification
        transaction_date=datetime.utcnow(),
        paid_at=datetime.utcnow()
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    # Update order status
    order.status = "paid"
    db.commit()

    return payment

def process_international_payment(payment_in: PaymentCreate, order: Order, db: Session):
    """Process USD payments via Stripe/PayPal"""
    if payment_in.currency != "USD":
        raise HTTPException(status_code=400, detail="USD required for international payments")

    payment = Payment(
        order_id=payment_in.order_id,
        method=payment_in.method,
        amount=payment_in.amount,
        currency="USD",
        status=PaymentStatus.PAID,
        transaction_date=datetime.utcnow(),
        paid_at=datetime.utcnow()
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    # Update order status
    order.status = "paid"
    db.commit()

    return payment

@router.post("/verify-bank-transfer/{payment_id}", response_model=PaymentOut)
def verify_bank_transfer(payment_id: int, db: Session = Depends(get_db)):
    """Admin endpoint to verify bank transfers"""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    payment.status = PaymentStatus.PAID
    payment.paid_at = datetime.utcnow()

    # Update order status
    order = db.query(Order).filter(Order.id == payment.order_id).first()
    order.status = "paid"

    db.commit()
    db.refresh(payment)

    return payment

@router.get("/{payment_id}", response_model=PaymentOut)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    """Get payment details"""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.get("/order/{order_id}", response_model=List[PaymentOut])
def get_order_payments(order_id: int, db: Session = Depends(get_db)):
    """Get all payments for an order"""
    payments = db.query(Payment).filter(Payment.order_id == order_id).all()
    return payments