from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date, datetime, UTC, timedelta
from .. import models, schemas
from ..database import SessionLocal, get_db
from ..dependencies.roles import role_required

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=schemas.OrderRead, dependencies=[Depends(role_required("cashier"))])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    discount_applied = False
    final_price = product.price
    if product.created_at < datetime.now(UTC) - timedelta(days=30):
        final_price *= 0.8
        discount_applied = True

    db_order = models.Order(product_id=product.id, final_price=final_price, discount_applied=discount_applied)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order

@router.patch("/{order_id}/status", response_model=schemas.OrderRead, dependencies=[Depends(role_required("consultant"))])
def update_order_status(order_id: int, status: schemas.OrderUpdateStatus, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status.status
    db.commit()
    db.refresh(order)
    return order

@router.get("/", response_model=list[schemas.OrderRead])
def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()

@router.post("/{order_id}/pay", response_model=schemas.OrderRead, dependencies=[Depends(role_required("cashier"))])
def pay_for_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = "paid"
    db.commit()
    db.refresh(order)
    return order

@router.get("/report", response_model=list[schemas.OrderRead], dependencies=[Depends(role_required("accountant"))])
def get_orders_report(
    from_date: date = Query(..., alias="from"),
    to_date: date = Query(..., alias="to"),
    db: Session = Depends(get_db)
):
    return db.query(models.Order)\
             .filter(models.Order.created_at >= from_date)\
             .filter(models.Order.created_at <= to_date)\
             .all()