import factory
from datetime import datetime
from factory.alchemy import SQLAlchemyModelFactory
from app.models import Product
from app.enums import Currency
from tests.db import TestingSessionLocal

class ProductFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Product
        sqlalchemy_session = TestingSessionLocal()
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('word')
    price = factory.Faker('pyint')
    currency = factory.Iterator([c.value for c in Currency])
    created_at = factory.LazyFunction(datetime.now)
