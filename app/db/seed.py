from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.models import Customer, Payment, Invoice, SupportTicket
def seed_customer_data(db: Session):
    customer = db.query(Customer).filter(Customer.email == "customer2@example.com").first()
    if not customer:
        return
    payment = db.query(Payment).filter(Payment.transaction_id == "TXN-DEMO-001").first()
    if not payment:
        payment = Payment(
            customer_id=customer.id,
            amount=Decimal("49.99"),
            status="failed",
            failure_reason="Insufficient funds",
            transaction_id="TXN-DEMO-001",
        )
        db.add(payment)
    invoice = db.query(Invoice).filter(Invoice.invoice_number == "INV-DEMO-001").first()
    if not invoice:
        invoice = Invoice(
            customer_id=customer.id,
            invoice_number="INV-DEMO-001",
            amount=Decimal("49.99"),
            status="unpaid",
        )
        db.add(invoice)
    ticket = db.query(SupportTicket).filter(
        SupportTicket.subject == "Demo support ticket"
    ).first()
    if not ticket:
        ticket = SupportTicket(
            customer_id=customer.id,
            subject="Demo support ticket",
            description="Demo ticket for testing the AI customer support agent.",
            status="open",
            priority="medium",
        )
        db.add(ticket)
    db.commit()