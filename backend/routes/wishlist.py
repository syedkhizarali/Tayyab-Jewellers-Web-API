# backend/routes/wishlist.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import Wishlist, Product
from backend.schemas import WishlistCreate, WishlistResponse
from backend.routes.auth import get_current_user  # Adjust if your project uses another auth dependency

router = APIRouter(prefix="/wishlist", tags=["wishlist"])

@router.get("/", response_model=List[WishlistResponse])
def list_wishlist(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    items = db.query(Wishlist).filter(Wishlist.user_id == current_user.id).all()
    return items

@router.post("/", response_model=WishlistResponse, status_code=status.HTTP_201_CREATED)
def add_wishlist(item_in: WishlistCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # check product exists
    product = db.query(Product).filter(Product.id == item_in.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    already = db.query(Wishlist).filter(Wishlist.user_id == current_user.id, Wishlist.product_id == item_in.product_id).first()
    if already:
        return already

    obj = Wishlist(user_id=current_user.id, product_id=item_in.product_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wishlist(item_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    item = db.query(Wishlist).filter(Wishlist.id == item_id, Wishlist.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(item)
    db.commit()
    return None
