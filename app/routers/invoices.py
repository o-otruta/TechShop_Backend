from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal
from ..dependencies.roles import role_required

router = APIRouter(prefix="/invoices", tags=["Invoices"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create/{order_id}", response_model=schemas.InvoiceRead, dependencies=[Depends(role_required("cashier"))])
def create_invoice(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    invoice = models.Invoice(order_id=order_id)
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

@router.get("/", response_model=list[schemas.InvoiceRead])
def get_all_invoices(db: Session = Depends(get_db)):
    return db.query(models.Invoice).all()
