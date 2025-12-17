# routes/profile.py

import os
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.security import get_current_user
from backend.reprossitories.profile_repo import (
    get_profile, create_profile, update_profile, update_profile_photo
)
from backend.schemas import UserProfileCreate, UserProfileUpdate, UserProfileResponse

router = APIRouter(prefix="/profile", tags=["User Profile"])

UPLOAD_DIR = "uploads/profiles"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/me", response_model=UserProfileResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    profile = get_profile(db, user.id)
    if not profile:
        return create_profile(db, user.id, UserProfileCreate())
    return profile

@router.put("/me", response_model=UserProfileResponse)
def update_my_profile(
    data: UserProfileUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    profile = update_profile(db, user.id, data)
    return profile

@router.post("/upload-photo", response_model=UserProfileResponse)
def upload_photo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    file_ext = file.filename.split(".")[-1]
    filename = f"user_{user.id}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return update_profile_photo(db, user.id, filename)
