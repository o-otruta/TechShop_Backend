from sqlalchemy import Column, Boolean, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from .database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.now(UTC))

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    status = Column(String, default="created")  # created, done, paid
    created_at = Column(DateTime, default=datetime.now(UTC))
    final_price = Column(Float)
    discount_applied = Column(Boolean, default=False)

    product = relationship("Product")

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    invoice_date = Column(DateTime, default=datetime.now(UTC))

    order = relationship("Order")
