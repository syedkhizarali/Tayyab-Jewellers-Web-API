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
    inventory,
    wishlist,
    address,
    profile
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

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
app.include_router(profile.router)
app.include_router(address.router)
app.include_router(wishlist.router)
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
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173",
#     "https://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite/Vue (your original)
        "http://localhost:3000",   # React
        "http://localhost:5500",   # VS Code Live Server
        "http://127.0.0.1:5500",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "null",  # for file:// (some browsers)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend files
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
