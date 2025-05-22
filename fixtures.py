from app.database import SessionLocal, engine
from app.models import Product, Base
from datetime import datetime, timedelta
from app.enums import Currency

Base.metadata.create_all(bind=engine)

def seed_products():
    db = SessionLocal()

    if db.query(Product).first():
        print("Products already seeded")
        db.close()
        return

    now = datetime.now()
    items = [
        Product(name="TV", price=999999, currency=Currency.UAH, created_at=now),
        Product(name="Laptop", price=1899900, currency=Currency.UAH, created_at=now - timedelta(days=55)),
        Product(name="Pad", price=699999, currency=Currency.UAH, created_at=now),
        Product(name="Mouse", price=849900, currency=Currency.UAH, created_at=now - timedelta(days=99)),
        Product(name="Keyboard", price=199900, currency=Currency.UAH, created_at=now),
    ]

    db.add_all(items)
    db.commit()
    db.close()
    print("Seeded 5 products")

if __name__ == "__main__":
    seed_products()
