# routes/address.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.security import get_current_user  # adjust import path if different
from backend.reprossitories.address_repo import (
    get_addresses_by_user, get_address, create_address, update_address, delete_address
)
from backend.schemas import AddressCreate, AddressResponse, AddressUpdate

router = APIRouter(prefix="/addresses", tags=["addresses"])

@router.get("/me", response_model=List[AddressResponse])
def list_my_addresses(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_addresses_by_user(db, user.id)

@router.get("/me/{address_id}", response_model=AddressResponse)
def get_my_address(address_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    address = get_address(db, user.id, address_id)
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    return address

@router.post("/me", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_my_address(payload: AddressCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_address(db, user.id, payload)

@router.put("/me/{address_id}", response_model=AddressResponse)
def update_my_address(address_id: int, payload: AddressUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    address = update_address(db, user.id, address_id, payload)
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    return address

@router.delete("/me/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_address(address_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    ok = delete_address(db, user.id, address_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    return None
