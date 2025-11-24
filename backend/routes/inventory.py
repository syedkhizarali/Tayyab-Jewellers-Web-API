# app/routes/inventory.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from backend.database import get_db
from backend.models import Product
from backend.security import require_admin

router = APIRouter(prefix="/inventory", tags=["inventory"])

# Set up logger
logger = logging.getLogger("jewellery_api")

@router.put("/products/{product_id}/stock")
def update_stock(
        product_id: int,
        adjustment: int,  # Positive for addition, negative for deduction
        db: Session = Depends(get_db),
        admin=Depends(require_admin)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    new_stock = product.stock_quantity + adjustment
    if new_stock < 0:
        raise HTTPException(400, "Insufficient stock")

    product.stock_quantity = new_stock
    db.commit()

    logger.info(f"Stock updated for product {product_id} ({product.name}): {adjustment}. New stock: {new_stock}")

    return {
        "message": "Stock updated successfully",
        "product_id": product_id,
        "product_name": product.name,
        "adjustment": adjustment,
        "new_stock": new_stock
    }


@router.get("/low-stock")
def get_low_stock_products(
        threshold: int = 5,  # Default threshold for low stock
        db: Session = Depends(get_db),
        admin=Depends(require_admin)
):

    low_stock_products = db.query(Product).filter(
        Product.stock_quantity <= threshold
    ).all()

    return {
        "threshold": threshold,
        "count": len(low_stock_products),
        "products": [
            {
                "id": product.id,
                "name": product.name,
                "current_stock": product.stock_quantity,
                "category": product.category
            }
            for product in low_stock_products
        ]
    }


@router.get("/stock-history/{product_id}")
def get_stock_history(
        product_id: int,
        db: Session = Depends(get_db),
        admin=Depends(require_admin)
):
    """
    🆕 NEW ENDPOINT: Get stock history for a product

    - For auditing and tracking inventory changes
    - Admin authorization required
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    return {
        "product_id": product.id,
        "product_name": product.name,
        "current_stock": product.stock_quantity,
        "message": "For detailed history, implement StockHistory model"
    }