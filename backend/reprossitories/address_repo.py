# repositories/address_repo.py

from sqlalchemy.orm import Session
from typing import List, Optional
from backend.models import UserAddress
from backend.schemas import AddressCreate, AddressUpdate

def get_addresses_by_user(db: Session, user_id: int) -> List[UserAddress]:
    return db.query(UserAddress).filter(UserAddress.user_id == user_id).order_by(UserAddress.is_default.desc(), UserAddress.id.desc()).all()

def get_address(db: Session, user_id: int, address_id: int) -> Optional[UserAddress]:
    return db.query(UserAddress).filter(UserAddress.user_id == user_id, UserAddress.id == address_id).first()

def create_address(db: Session, user_id: int, addr: AddressCreate) -> UserAddress:
    # if setting is_default True, unset other defaults
    if addr.is_default:
        db.query(UserAddress).filter(UserAddress.user_id == user_id).update({"is_default": False})
    address = UserAddress(user_id=user_id, **addr.dict())
    db.add(address)
    db.commit()
    db.refresh(address)
    return address

def update_address(db: Session, user_id: int, address_id: int, addr: AddressUpdate) -> Optional[UserAddress]:
    address = get_address(db, user_id, address_id)
    if not address:
        return None
    data = addr.dict(exclude_unset=True)
    if data.get("is_default"):
        db.query(UserAddress).filter(UserAddress.user_id == user_id).update({"is_default": False})
    for k, v in data.items():
        setattr(address, k, v)
    db.commit()
    db.refresh(address)
    return address

def delete_address(db: Session, user_id: int, address_id: int) -> bool:
    address = get_address(db, user_id, address_id)
    if not address:
        return False
    db.delete(address)
    db.commit()
    return True
