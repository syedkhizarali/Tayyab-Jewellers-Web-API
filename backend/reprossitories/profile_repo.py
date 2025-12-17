# repositories/profile_repo.py

from sqlalchemy.orm import Session
from backend.models import UserProfile
from backend.schemas import UserProfileCreate, UserProfileUpdate

def get_profile(db: Session, user_id: int):
    return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

def create_profile(db: Session, user_id: int, data: UserProfileCreate):
    profile = UserProfile(user_id=user_id, **data.dict())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

def update_profile(db: Session, user_id: int, data: UserProfileUpdate):
    profile = get_profile(db, user_id)
    if not profile:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(profile, field, value)
    db.commit()
    db.refresh(profile)
    return profile

def update_profile_photo(db: Session, user_id: int, file_path: str):
    profile = get_profile(db, user_id)
    if not profile:
        return None
    profile.profile_photo = file_path
    db.commit()
    db.refresh(profile)
    return profile
