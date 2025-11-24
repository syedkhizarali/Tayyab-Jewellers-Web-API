from sqlalchemy.orm import Session

from backend.models import Product

def get_recommendations(product_id: int, db: Session, limit: int = 4):
    current_product = db.query(Product).filter(Product.id == product_id).first()
    if not current_product:
        return []

    # Recommend similar products (same category, metal, similar price)
    similar = db.query(Product).filter(
        Product.id != product_id,
        Product.metal_type == current_product.metal_type,
        Product.category == current_product.category,
        Product.price.between(current_product.price * 0.7, current_product.price * 1.3)
    ).limit(limit).all()

    return similar