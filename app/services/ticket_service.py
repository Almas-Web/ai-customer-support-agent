from sqlalchemy.orm import Session
from app.models.models import SupportTicket
from app.schems.ticket import TicketCreate
def create_ticket(db: Session, ticket_data: TicketCreate):
    ticket = SupportTicket(
        customer_id=ticket_data.customer_id,
        subject=ticket_data.subject,
        description=ticket_data.description,
        priority=ticket_data.priority,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket
def get_ticket_by_id(db: Session, ticket_id: int, customer_id: int):
    return (
        db.query(SupportTicket)
        .filter(
            SupportTicket.id == ticket_id,
            SupportTicket.customer_id == customer_id,
        )
        .first()
    )
def get_customer_tickets(db: Session, customer_id: int):
    return (
        db.query(SupportTicket)
        .filter(SupportTicket.customer_id == customer_id)
        .order_by(SupportTicket.created_at.desc())
        .all()
    )
def update_ticket_status(
    db: Session,
    ticket_id: int,
    customer_id: int,
    status: str,
):
    ticket = get_ticket_by_id(db, ticket_id, customer_id)
    if not ticket:
        return None
    ticket.status = status
    db.commit()
    db.refresh(ticket)
    return ticket