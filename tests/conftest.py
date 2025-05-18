import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Product
from datetime import datetime, timedelta

client = TestClient(app)

@pytest.fixture
def client_auth_cashier():
    return {"Authorization": "Bearer cashier"}

@pytest.fixture
def client_auth_consultant():
    return {"Authorization": "Bearer consultant"}

@pytest.fixture
def client_auth_accountant():
    return {"Authorization": "Bearer accountant"}

@pytest.fixture
def old_product():
    response = client.post("/products/", json={
        "name": "Laptop",
        "price": 1234.56
    })
    product = response.json()

    db = SessionLocal()
    db_product = db.query(Product).get(product["id"])
    db_product.created_at = datetime.utcnow() - timedelta(days=40)
    db.commit()
    db.close()
    return product
