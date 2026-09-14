from sqlalchemy.orm import Session
from app.models.models import Payment


def get_payment_by_id(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.id == payment_id).first()


def get_customer_payments(db: Session, customer_id: int):
    return (
        db.query(Payment)
        .filter(Payment.customer_id == customer_id)
        .order_by(Payment.created_at.desc())
        .all()
    )


def get_latest_payment(db: Session, customer_id: int):
    return (
        db.query(Payment)
        .filter(Payment.customer_id == customer_id)
        .order_by(Payment.created_at.desc())
        .first()
    )


def get_failed_payments(db: Session, customer_id: int):
    return (
        db.query(Payment)
        .filter(
            Payment.customer_id == customer_id,
            Payment.status == "failed",
        )
        .order_by(Payment.created_at.desc())
        .all()
    )