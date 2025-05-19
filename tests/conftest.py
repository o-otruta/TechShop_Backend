import os
import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.models import Product
from fastapi.testclient import TestClient
from app.main import app

engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    if os.path.exists("test.db"):
        os.remove("test.db")
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

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

    db = TestingSessionLocal()
    db_product = db.get(Product, product["id"])
    db_product.created_at = datetime.now() - timedelta(days=40)
    db.commit()
    db.close()
    return product
