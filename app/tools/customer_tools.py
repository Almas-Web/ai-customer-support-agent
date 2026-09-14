from sqlalchemy.orm import Session
from app.services.customer_service import (
    get_customer_by_id,
    get_customer_by_email,
)


def get_customer(
    db: Session,
    customer_id: int | None = None,
    email: str | None = None,
):
    if customer_id is not None:
        customer = get_customer_by_id(db, customer_id)
    elif email is not None:
        customer = get_customer_by_email(db, email)
    else:
        return {
            "success": False,
            "error": "Customer ID or email is required.",
        }

    if not customer:
        return {
            "success": False,
            "error": "Customer not found.",
        }

    return {
        "success": True,
        "customer": {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
        },
    }