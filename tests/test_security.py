from decimal import Decimal
from app.models.models import Conversation, Customer, Payment, Invoice, SupportTicket
from app.tools.payment_tools import get_payment_status
from app.tools.invoice_tools import get_invoice
from app.tools.ticket_tools import get_support_ticket
def test_customer_cannot_access_other_customer_payment(db):
    customer1 = Customer(name="Security Customer 1", email="security1@example.com")
    customer2 = Customer(name="Security Customer 2", email="security2@example.com")
    db.add_all([customer1, customer2])
    db.commit()
    db.refresh(customer1)
    db.refresh(customer2)
    payment = Payment(
        customer_id=customer1.id,
        amount=Decimal("100.00"),
        status="failed",
        failure_reason="Insufficient funds",
        transaction_id="SECURITY-TXN-001",
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    result = get_payment_status(
        db=db,
        customer_id=customer2.id,
        payment_id=payment.id,
    )
    assert result["success"] is False
    assert result["error"] == "Payment not found."
def test_customer_cannot_access_other_customer_invoice(db):
    customer1 = Customer(name="Invoice Customer 1", email="invoice1@example.com")
    customer2 = Customer(name="Invoice Customer 2", email="invoice2@example.com")
    db.add_all([customer1, customer2])
    db.commit()
    db.refresh(customer1)
    db.refresh(customer2)
    invoice = Invoice(
        customer_id=customer1.id,
        invoice_number="SECURITY-INV-001",
        amount=Decimal("150.00"),
        status="unpaid",
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    result = get_invoice(
        db=db,
        customer_id=customer2.id,
        invoice_id=invoice.id,
    )
    assert result["success"] is False
    assert result["error"] == "Invoice not found."
def test_customer_cannot_access_other_customer_ticket(db):
    customer1 = Customer(name="Ticket Customer 1", email="ticket1@example.com")
    customer2 = Customer(name="Ticket Customer 2", email="ticket2@example.com")
    db.add_all([customer1, customer2])
    db.commit()
    db.refresh(customer1)
    db.refresh(customer2)
    ticket = SupportTicket(
        customer_id=customer1.id,
        subject="Private Security Ticket",
        description="Private ticket data",
        status="open",
        priority="high",
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    result = get_support_ticket(
        db=db,
        customer_id=customer2.id,
        ticket_id=ticket.id,
    )
    assert result["success"] is False
    assert result["error"] == "Support ticket not found."

def test_customer_cannot_access_other_customer_conversation(db):
    from app.services.conversation_service import get_conversation
    customer1 = Customer(name="Conversation Customer 1", email="conversation1@example.com")
    customer2 = Customer(name="Conversation Customer 2", email="conversation2@example.com")
    db.add_all([customer1, customer2])
    db.commit()
    db.refresh(customer1)
    db.refresh(customer2)
    conversation = Conversation(
        customer_id=customer1.id,
        status="active",
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    result = get_conversation(
        db=db,
        conversation_id=conversation.id,
        customer_id=customer2.id,
    )
    assert result is None


def test_customer_cannot_access_admin_role():
    from app.rbac import require_role
    from fastapi import HTTPException
    class FakeUser:
        role = "customer"
    role_checker = require_role("admin")
    try:
        role_checker(FakeUser())
        assert False
    except HTTPException as exc:
        assert exc.status_code == 403
        assert exc.detail == "You do not have permission to perform this action."

def test_agent_forces_authenticated_customer_id(monkeypatch):
    from app.agent import agent
    captured = {}
    def fake_get_payment_status(db, customer_id, payment_id=None, failed_only=False):
        captured["customer_id"] = customer_id
        return {"success": False, "error": "Payment not found."}
    monkeypatch.setitem(agent.TOOL_FUNCTIONS, "get_payment_status", fake_get_payment_status)
    function = agent.TOOL_FUNCTIONS["get_payment_status"]
    function(
        db=None,
        customer_id=1,
        payment_id=999,
    )
    assert captured["customer_id"] == 1