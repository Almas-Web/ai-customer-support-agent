from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies import get_current_user
from app.models.models import Customer, User
from app.schems.order import OrderCreate, OrderResponse, OrderCheckoutResponse
from app.services.order_service import (
    create_order_checkout,
    get_customer_orders,
    get_order_by_id,
)

router = APIRouter(prefix="/orders", tags=["Orders"])
@router.post(
    "/",
    response_model=OrderCheckoutResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    customer = (
        db.query(Customer)
        .filter(Customer.user_id == current_user.id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer profile not found.",
        )

    result = create_order_checkout(
        db=db,
        customer_id=customer.id,
        item_name=order_data.item_name,
        amount=order_data.amount,
    )

    return {
        "order": result["order"],
        "payment": {
            "id": result["payment"].id,
            "customer_id": result["payment"].customer_id,
            "order_id": result["payment"].order_id,
            "amount": result["payment"].amount,
            "status": result["payment"].status,
            "transaction_id": result["payment"].transaction_id,
            "failure_reason": result["payment"].failure_reason,
            "created_at": result["payment"].created_at,
        },
        "invoice": {
            "id": result["invoice"].id,
            "customer_id": result["invoice"].customer_id,
            "order_id": result["invoice"].order_id,
            "invoice_number": result["invoice"].invoice_number,
            "amount": result["invoice"].amount,
            "status": result["invoice"].status,
            "created_at": result["invoice"].created_at,
        },
    }


@router.get(
    "/me",
    response_model=list[OrderResponse],
)
def get_my_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    customer = (
        db.query(Customer)
        .filter(Customer.user_id == current_user.id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer profile not found.",
        )

    return get_customer_orders(db, customer.id)


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
def get_my_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    customer = (
        db.query(Customer)
        .filter(Customer.user_id == current_user.id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer profile not found.",
        )

    order = get_order_by_id(
        db=db,
        order_id=order_id,
        customer_id=customer.id,
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found.",
        )

    return order