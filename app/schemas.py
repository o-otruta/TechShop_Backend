from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.enums import Currency, OrderStatus

class ProductBase(BaseModel):
    name: str
    price: int
    currency: Currency

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class OrderBase(BaseModel):
    product_id: int

class OrderCreate(OrderBase):
    pass

class OrderUpdateStatus(BaseModel):
    status: OrderStatus

class OrderRead(BaseModel):
    id: int
    product: ProductRead
    final_price: int
    discount_applied: bool
    status: OrderStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InvoiceRead(BaseModel):
    id: int
    invoice_date: datetime
    order: OrderRead

    model_config = ConfigDict(from_attributes=True)

