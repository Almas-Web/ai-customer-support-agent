from app.tools.customer_tools import get_customer
from app.tools.payment_tools import get_payment_status
from app.tools.invoice_tools import get_invoice
from app.tools.ticket_tools import create_support_ticket
from app.tools.email_tools import send_email


TOOLS = {
    "get_customer": get_customer,
    "get_payment_status": get_payment_status,
    "get_invoice": get_invoice,
    "create_support_ticket": create_support_ticket,
    "send_email": send_email,
}