from sqlalchemy.orm import Session
from app.services.order_service import get_order_by_id, get_customer_orders
def get_order(
    db: Session,
    customer_id: int,
    order_id: int | None = None,
):
    if order_id is not None:
        order = get_order_by_id(
            db=db,
            order_id=order_id,
            customer_id=customer_id,
        )
        if not order:
            return {
                "success": False,
                "error": "Order not found.",
            }
        return {
            "success": True,
            "order": {
                "id": order.id,
                "customer_id": order.customer_id,
                "item_name": order.item_name,
                "amount": str(order.amount),
                "status": order.status,
                "created_at": order.created_at.isoformat(),
            },
        }
    orders = get_customer_orders(
        db=db,
        customer_id=customer_id,
    )
    if not orders:
        return {
            "success": False,
            "error": "No order found.",
        }
    return {
        "success": True,
        "orders": [
            {
                "id": order.id,
                "item_name": order.item_name,
                "amount": str(order.amount),
                "status": order.status,
                "created_at": order.created_at.isoformat(),
            }
            for order in orders
        ],
    }