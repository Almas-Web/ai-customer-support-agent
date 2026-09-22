from decimal import Decimal
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.models import Order, Payment, Invoice

def create_order_checkout(
    db: Session,
    customer_id: int,
    item_name: str,
    amount: Decimal,
):
    order = Order(
        customer_id=customer_id,
        item_name=item_name,
        amount=amount,
        status="paid",
    )

    db.add(order)
    db.flush()

    payment = Payment(
        customer_id=customer_id,
        order_id=order.id,
        amount=amount,
        status="paid",
        failure_reason=None,
        transaction_id=f"TXN-{uuid4().hex[:12].upper()}",
    )

    db.add(payment)

    invoice = Invoice(
        customer_id=customer_id,
        order_id=order.id,
        invoice_number=f"INV-{uuid4().hex[:12].upper()}",
        amount=amount,
        status="paid",
    )

    db.add(invoice)

    db.commit()

    db.refresh(order)
    db.refresh(payment)
    db.refresh(invoice)

    return {
        "order": order,
        "payment": payment,
        "invoice": invoice,
    }


def get_customer_orders(
    db: Session,
    customer_id: int,
):
    return (
        db.query(Order)
        .filter(Order.customer_id == customer_id)
        .order_by(Order.created_at.desc())
        .all()
    )


def get_order_by_id(
    db: Session,
    order_id: int,
    customer_id: int,
):
    return (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.customer_id == customer_id,
        )
        .first()
    )