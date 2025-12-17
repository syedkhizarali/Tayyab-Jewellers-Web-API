# backend/models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Date
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base
from backend.schemas import PaymentMethod, PaymentStatus

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120))
    email = Column(String(150), unique=True, index=True, nullable=False)
    phone = Column(String(30), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    addresses = relationship("UserAddress", back_populates="user", cascade="all, delete-orphan")
    wishlist_items = relationship("Wishlist", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

    role = Column(String(30), default="user")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    metal_type = Column(String(20), nullable=False)
    category = Column(String(50), default="ready made")
    karat = Column(Integer, default=24)
    weight_grams = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    making_charge = Column(Float, default=0.0)
    stock_quantity = Column(Integer, default=0)
    description = Column(Text, nullable=True)
    images = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String(50), default="pending")
    total_price = Column(Float, default=0.0)
    delivery_address = Column(Text, nullable=True)
    delivery_region = Column(String(100), nullable=True)
    placed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, default=0.0)
    total_price = Column(Float, default=0.0)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    method = Column(SAEnum(PaymentMethod))
    amount = Column(Float)
    status = Column(SAEnum(PaymentStatus), default=PaymentStatus.PENDING)
    # For bank transfers
    bank_name = Column(String(100), nullable=True)
    account_number = Column(String(50), nullable=True)
    transaction_id = Column(String(100), nullable=True)
    transaction_date = Column(DateTime, nullable=True)
    # For digital payments
    payment_gateway_id = Column(String(100), nullable=True)
    currency = Column(String(10), default="PKR")
    paid_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class GoldRate(Base):
    __tablename__ = "gold_rates"
    id = Column(Integer, primary_key=True)
    karat = Column(Integer, nullable=False)
    price_per_tola = Column(Float, nullable=False)
    price_per_gram = Column(Float, nullable=False)
    source = Column(String(50), default="live")
    created_at = Column(DateTime, default=datetime.utcnow)


class GoldRateHistory(Base):
    __tablename__ = "gold_rate_history"
    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    karat = Column(Integer, nullable=False)
    avg_price_per_tola = Column(Float, nullable=False)
    avg_price_per_gram = Column(Float, nullable=False)


class GoldAnalysisPost(Base):
    __tablename__ = "gold_analysis_posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    tags = Column(String(200))
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = relationship("User")


class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    phone = Column(String(20), nullable=True)
    dob = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)
    profile_photo = Column(String(255), nullable=True)

    user = relationship("User", back_populates="profile")


class UserAddress(Base):
    __tablename__ = "user_addresses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    full_name = Column(String(200), nullable=True)
    phone = Column(String(50), nullable=True)
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(50), nullable=True)
    country = Column(String(100), nullable=True)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="addresses")


class Wishlist(Base):
    __tablename__ = "wishlists"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="wishlist_items")
    product = relationship("Product")
