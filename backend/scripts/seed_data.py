from backend.database import SessionLocal, engine
from backend.models import Base, Product, User
from backend.utils.hashing import hash_password

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# create admin
admin = User(name="Admin", email="admin@tayyab.com", hashed_password=hash_password("admin pass"), is_admin=True)
db.add(admin)

# sample products
p1 = Product(name="24K Gold Ring", metal_type="gold", karat=24, weight_grams=5.0, price=200000, stock_quantity=3)
p2 = Product(name="22K Ready made Set", metal_type="gold", karat=22, weight_grams=20.0, price=730000, stock_quantity=2)
db.add_all([p1,p2])
db.commit()
db.close()
print("Seeded")
