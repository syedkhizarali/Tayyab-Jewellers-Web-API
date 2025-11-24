from fastapi import APIRouter, Depends, HTTPException,UploadFile,File
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Product
from backend.schemas import ProductCreate, ProductOut
from backend.security import require_admin  # use admin-only dependency
import os ,shutil
from backend.schemas import ProductFilter
from backend.services.cache import cache_response

UPLOAD_DIR = "uploads/products"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=list[ProductOut])
@cache_response(ttl=60)  # Cache for 1 minute
def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@router.post("/", response_model=ProductOut)
def create_product(prod_in: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**prod_in.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.post("/upload-image/{product_id}")
async def upload_product_image(product_id: int, file: UploadFile = File(...), admin=Depends(require_admin), db: Session = Depends(get_db)):
    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in ("jpg","jpeg","png","webp"):
        raise HTTPException(400, "Invalid file type")
    filename = f"{product_id}.{ext}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save filename in Product.images (comma-separated or JSON). Here simple overwrite:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")
    product.images = filename
    db.commit()
    db.refresh(product)

    return {"url": f"/static/products/{filename}", "filename": filename}


@router.get("/search", response_model=list[ProductOut])
def search_products(
        query: str = None,
        filters: ProductFilter = Depends(),
        db: Session = Depends(get_db)
):
    base_query = db.query(Product)

    # Text search
    if query:
        base_query = base_query.filter(
            Product.name.ilike(f"%{query}%") |
            Product.description.ilike(f"%{query}%")
        )

    # Apply filters
    if filters.min_price:
        base_query = base_query.filter(Product.price >= filters.min_price)
    if filters.max_price:
        base_query = base_query.filter(Product.price <= filters.max_price)
    if filters.metal_type:
        base_query = base_query.filter(Product.metal_type == filters.metal_type)
    if filters.karat:
        base_query = base_query.filter(Product.karat == filters.karat)
    if filters.category:
        base_query = base_query.filter(Product.category == filters.category)
    if filters.in_stock:
        base_query = base_query.filter(Product.stock_quantity > 0)

    return base_query.all()


