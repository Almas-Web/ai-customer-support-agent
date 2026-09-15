from sqlalchemy.orm import Session
from app.services.payment_service import (
    get_payment_by_id,
    get_latest_payment,
    get_failed_payments,
)
def get_payment_status(
    db: Session,
    customer_id: int,
    payment_id: int | None = None,
    failed_only: bool = False,
):
    if payment_id is not None:
        payment = get_payment_by_id(db, payment_id, customer_id)
        if not payment:
            return {
                "success": False,
                "error": "Payment not found.",
            }
        return {
            "success": True,
            "payment": {
                "id": payment.id,
                "customer_id": payment.customer_id,
                "amount": str(payment.amount),
                "status": payment.status,
                "failure_reason": payment.failure_reason,
                "transaction_id": payment.transaction_id,
                "created_at": payment.created_at.isoformat(),
            },
        }
    if failed_only:
        payments = get_failed_payments(db, customer_id)
    else:
        payment = get_latest_payment(db, customer_id)
        payments = [payment] if payment else []
    if not payments:
        return {
            "success": False,
            "error": "No payment found.",
        }
    return {
        "success": True,
        "payments": [
            {
                "id": payment.id,
                "amount": str(payment.amount),
                "status": payment.status,
                "failure_reason": payment.failure_reason,
                "transaction_id": payment.transaction_id,
                "created_at": payment.created_at.isoformat(),
            }
            for payment in payments
        ],
    }