from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Body
from backend.models import User
from backend.database import get_db
from backend.security import get_current_user, create_access_token, _decode_token
from backend.configs import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "phone": current_user.phone,
        "is_admin": current_user.is_admin,
        "role": current_user.role
    }

@router.post("/refresh")
def refresh_token(refresh_token: str = Body(..., embed=True)):
    try:
        payload = _decode_token(refresh_token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except HTTPException:
        raise
    access_token = create_access_token({"sub": str(user_id)}, expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {"access_token": access_token, "token_type": "bearer"}
