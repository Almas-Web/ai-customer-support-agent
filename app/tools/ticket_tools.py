from sqlalchemy.orm import Session
from app.services.ticket_service import (
    create_ticket,
    get_ticket_by_id,
    get_customer_tickets,
)
from app.schems.ticket import TicketCreate


def create_support_ticket(
    db: Session,
    customer_id: int,
    subject: str,
    description: str,
    priority: str = "medium",
):
    ticket_data = TicketCreate(
        customer_id=customer_id,
        subject=subject,
        description=description,
        priority=priority,
    )

    ticket = create_ticket(db, ticket_data)

    return {
        "success": True,
        "ticket": {
            "id": ticket.id,
            "customer_id": ticket.customer_id,
            "subject": ticket.subject,
            "description": ticket.description,
            "status": ticket.status,
            "priority": ticket.priority,
            "created_at": ticket.created_at.isoformat(),
        },
    }


def get_support_ticket(
    db: Session,
    ticket_id: int,
):
    ticket = get_ticket_by_id(db, ticket_id)

    if not ticket:
        return {
            "success": False,
            "error": "Support ticket not found.",
        }

    return {
        "success": True,
        "ticket": {
            "id": ticket.id,
            "customer_id": ticket.customer_id,
            "subject": ticket.subject,
            "description": ticket.description,
            "status": ticket.status,
            "priority": ticket.priority,
            "created_at": ticket.created_at.isoformat(),
        },
    }


def get_customer_support_tickets(
    db: Session,
    customer_id: int,
):
    tickets = get_customer_tickets(db, customer_id)

    return {
        "success": True,
        "tickets": [
            {
                "id": ticket.id,
                "subject": ticket.subject,
                "status": ticket.status,
                "priority": ticket.priority,
                "created_at": ticket.created_at.isoformat(),
            }
            for ticket in tickets
        ],
    }