from pydantic import BaseModel
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    price: float

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    product_id: int

class OrderCreate(OrderBase):
    pass

class OrderUpdateStatus(BaseModel):
    status: str

class OrderRead(BaseModel):
    id: int
    product: ProductRead
    final_price: float
    discount_applied: bool
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


class InvoiceRead(BaseModel):
    id: int
    invoice_date: datetime
    order: OrderRead

    class Config:
        orm_mode = True
