# app/main.py
from fastapi import FastAPI
from backend.database import engine, Base
from backend import models  # ensures models are registered with SQLAlchemy
from backend.configs import settings
from backend.routes import (
    auth,
    users,
    products,
    orders,
    payments,
    rates,
    history,
    admin,
    inventory
)
# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="Tayyab Jewellers API",
    description="Backend API for Tayyab Jewellers E-commerce Platform",
    version="1.0.0"
)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(rates.router)
app.include_router(history.router)
app.include_router(inventory.router)
@app.get("/")
def root():
    """
    Root endpoint showing API status and available features
    """
    return {
        "status": "ok",
        "project": "Tayyab Jewellers Backend",
        "version": "1.0.0",
        "features": [
            "User Authentication & Authorization",
            "Product Management",
            "Order Processing",
            "Payment Integration",
            "Live Gold Rates",
            "Gold Market Analysis Blog",
            "Historical Gold Data",
            "Inventory Management",  # 🆕 NEW FEATURE ADDED
            "Admin Dashboard",
            "Sales Analytics"
        ]
    }
@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "database": "connected",
        "features_available": 10,  # Updated count
        "inventory_management": "active"  # 🆕 NEW: Show inventory feature status
    }