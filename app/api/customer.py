from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.dependencies import get_current_user
from app.models.models import Customer, User
from app.schems.customer import CustomerResponse
router = APIRouter(prefix="/customer", tags=["Customer"])
@router.get("/me", response_model=CustomerResponse)
def get_my_customer_profile(
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
    return customer