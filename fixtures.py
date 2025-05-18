from app.database import SessionLocal
from app.models import Product
from datetime import datetime, timedelta

def seed_products():
    db = SessionLocal()

    if db.query(Product).first():
        print("Products already seeded")
        db.close()
        return

    now = datetime.utcnow()
    items = [
        Product(name="TV", price=9999.99, created_at=now),
        Product(name="Laptop", price=18999.00, created_at=now - timedelta(days=55)),
        Product(name="Pad", price=6999.99, created_at=now),
        Product(name="Mouse", price=8499.00, created_at=now - timedelta(days=99)),
        Product(name="Keyboard", price=1999.00, created_at=now),
    ]

    db.add_all(items)
    db.commit()
    db.close()
    print("Seeded 5 products")

if __name__ == "__main__":
    seed_products()
