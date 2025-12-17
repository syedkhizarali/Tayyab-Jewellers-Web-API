# backend/schemas.py
from datetime import datetime, date
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from pydantic import ConfigDict

# --- Payment Enums ---
class PaymentMethod(str, Enum):
    BANK_TRANSFER = "bank_transfer"
    JAZZ_CASH = "jazz_cash"
    EASYPAISA = "easyPaisa"
    STRIPE = "stripe"
    PAYPAL = "paypal"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

# --- Users ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str]
    is_admin: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Products ---
class ProductCreate(BaseModel):
    name: str
    metal_type: str
    category: Optional[str] = "ready made"
    karat: int
    weight_grams: float
    making_charge: Optional[float] = 0.0
    stock_quantity: int
    description: Optional[str] = None
    price: Optional[float] = 0.0

class ProductOut(ProductCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Orders ---
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float

    model_config = ConfigDict(from_attributes=True)

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemCreate]
    delivery_address: Optional[str] = None
    delivery_region: Optional[str] = None

class OrderOut(BaseModel):
    id: int
    user_id: int
    status: str
    total_price: float
    delivery_address: Optional[str]
    delivery_region: Optional[str]
    placed_at: datetime
    items: List[OrderItemOut]

    model_config = ConfigDict(from_attributes=True)

# --- Token ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenWithRefresh(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# --- Payments ---
class PaymentCreate(BaseModel):
    order_id: int
    method: PaymentMethod
    amount: float
    currency: str = "PKR"
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    transaction_id: Optional[str] = None
    payment_token: Optional[str] = None

class PaymentOut(BaseModel):
    id: int
    order_id: int
    method: PaymentMethod
    amount: float
    status: PaymentStatus
    currency: str
    bank_name: Optional[str]
    transaction_id: Optional[str]
    paid_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

# --- Gold Rates ---
class GoldRateCreate(BaseModel):
    karat: int
    price_per_tola: float
    source: Optional[str] = "manual"

class GoldRateOut(BaseModel):
    id: int
    karat: int
    price_per_tola: float
    price_per_gram: float
    source: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Gold History ---
class GoldHistoryIn(BaseModel):
    year: int
    karat: int
    avg_price_per_tola: float

class UserUpdatePassword(BaseModel):
    old_password: str = Field(..., min_length=6, description="Current password for verification")
    new_password: str = Field(..., min_length=6, description="New password to set")

class GoldAnalysisCreate(BaseModel):
    title: str
    content: str
    tags: str = ""

class GoldAnalysisOut(GoldAnalysisCreate):
    id: int
    author_id: int
    is_published: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class GoldAnalysisWithAuthor(GoldAnalysisOut):
    author_name: str
    author_email: str

class ProductFilter(BaseModel):
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    metal_type: Optional[str] = None
    karat: Optional[int] = None
    category: Optional[str] = None
    in_stock: Optional[bool] = None

class UserProfileBase(BaseModel):
    phone: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileUpdate(UserProfileBase):
    pass

class UserProfileResponse(UserProfileBase):
    id: int
    profile_photo: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class AddressBase(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address_line1: str
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    is_default: Optional[bool] = False

class AddressCreate(AddressBase):
    pass

class AddressUpdate(AddressBase):
    pass

class AddressResponse(AddressBase):
    id: int
    user_id: int
    created_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

# Wishlist schemas
class WishlistBase(BaseModel):
    product_id: int

class WishlistCreate(WishlistBase):
    pass

class WishlistResponse(WishlistBase):
    id: int
    user_id: int
    added_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
