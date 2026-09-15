from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.dependencies import get_current_user
from app.models.models import Customer, User
from app.services.payment_service import get_customer_payments
from app.schems.payment import PaymentResponse
router = APIRouter(prefix="/payments", tags=["Payments"])
@router.get("/me", response_model=list[PaymentResponse])
def get_my_payments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    customer = db.query(Customer).filter(
        Customer.user_id == current_user.id
    ).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer profile not found.",
        )
    return get_customer_payments(db, customer.id)