from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

# --- Payment Enums ---
class PaymentMethod(str, Enum):
    BANK_TRANSFER = "bank_transfer"
    JAZZ_CASH = "jazz_cash"
    EASYPAISA = "easypaisa"
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

    class Config:
        from_attributes = True

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

    class Config:
        from_attributes = True

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

    class Config:
        from_attributes = True

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

    class Config:
        from_attributes = True

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
    # For bank transfers
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    transaction_id: Optional[str] = None
    # For digital payments
    payment_token: Optional[str] = None  # For Stripe/PayPal

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

    class Config:
        from_attributes = True

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

    class Config:
        from_attributes = True

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

    class Config:
        from_attributes = True

class GoldAnalysisWithAuthor(GoldAnalysisOut):
    author_name: str
    author_email: str
# Add this in your schemas.py after the Product classes
class ProductFilter(BaseModel):
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    metal_type: Optional[str] = None
    karat: Optional[int] = None
    category: Optional[str] = None
    in_stock: Optional[bool] = None