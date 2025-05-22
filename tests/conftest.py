import os
import pytest
from app.database import Base, get_db
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta
from tests.db import engine, TestingSessionLocal
from tests.factories import ProductFactory

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
def new_product():
    return ProductFactory()


@pytest.fixture
def old_product():
    return ProductFactory(created_at=datetime.now() - timedelta(days=40))
