from sqlalchemy import Column, Boolean, Integer, String, Enum as SqlEnum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.enums import Currency, OrderStatus
from .database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer)
    currency = Column(
        SqlEnum(
            Currency,
            name="currency",
            values_callable=lambda enum: [e.value for e in enum]
        ),
        nullable=False,
        default=Currency.UAH
    )
    created_at = Column(DateTime, default=datetime.now())

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    status = Column(
        SqlEnum(
            OrderStatus,
            name="order_status",
            values_callable=lambda enum: [e.value for e in enum]
        ),
        nullable=False,
        default=OrderStatus.CREATED
    )
    created_at = Column(DateTime, default=datetime.now())
    final_price = Column(Integer)
    discount_applied = Column(Boolean, default=False)

    product = relationship("Product")

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    invoice_date = Column(DateTime, default=datetime.now())

    order = relationship("Order")
