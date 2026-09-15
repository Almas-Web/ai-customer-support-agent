from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.dependencies import get_current_user
from app.models.models import Customer, User
from app.services.ticket_service import get_customer_tickets
from app.schems.ticket import TicketResponse
router = APIRouter(prefix="/tickets", tags=["Support Tickets"])
@router.get("/me", response_model=list[TicketResponse])
def get_my_tickets(
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
    return get_customer_tickets(db, customer.id)