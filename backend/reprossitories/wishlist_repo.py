# repositories/wishlist_repo.py

from sqlalchemy.orm import Session
from typing import List, Optional
from backend.models import Wishlist
from backend.schemas import WishlistCreate

def get_wishlist(db: Session, user_id: int) -> List[Wishlist]:
    return db.query(Wishlist).filter(Wishlist.user_id == user_id).order_by(Wishlist.added_at.desc()).all()

def get_wishlist_item(db: Session, user_id: int, product_id: int) -> Optional[Wishlist]:
    return db.query(Wishlist).filter(Wishlist.user_id == user_id, Wishlist.product_id == product_id).first()

def add_to_wishlist(db: Session, user_id: int, data: WishlistCreate) -> Wishlist:
    existing = get_wishlist_item(db, user_id, data.product_id)
    if existing:
        return existing
    item = Wishlist(user_id=user_id, product_id=data.product_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def remove_from_wishlist(db: Session, user_id: int, product_id: int) -> bool:
    item = get_wishlist_item(db, user_id, product_id)
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True
