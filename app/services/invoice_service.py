from sqlalchemy.orm import Session
from app.models.models import Invoice


def get_invoice_by_id(db: Session, invoice_id: int):
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()


def get_customer_invoices(db: Session, customer_id: int):
    return (
        db.query(Invoice)
        .filter(Invoice.customer_id == customer_id)
        .order_by(Invoice.created_at.desc())
        .all()
    )


def get_latest_invoice(db: Session, customer_id: int):
    return (
        db.query(Invoice)
        .filter(Invoice.customer_id == customer_id)
        .order_by(Invoice.created_at.desc())
        .first()
    )


def get_unpaid_invoices(db: Session, customer_id: int):
    return (
        db.query(Invoice)
        .filter(
            Invoice.customer_id == customer_id,
            Invoice.status.in_(["unpaid", "overdue"]),
        )
        .order_by(Invoice.created_at.desc())
        .all()
    )