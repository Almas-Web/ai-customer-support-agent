from sqlalchemy.orm import Session
from app.services.invoice_service import (
    get_invoice_by_id,
    get_latest_invoice,
    get_unpaid_invoices,
)
def get_invoice(
    db: Session,
    customer_id: int,
    invoice_id: int | None = None,
    unpaid_only: bool = False,
):
    if invoice_id is not None:
        invoice = get_invoice_by_id(db, invoice_id, customer_id)
        if not invoice:
            return {
                "success": False,
                "error": "Invoice not found.",
            }
        return {
            "success": True,
            "invoice": {
                "id": invoice.id,
                "invoice_number": invoice.invoice_number,
                "amount": str(invoice.amount),
                "status": invoice.status,
                "created_at": invoice.created_at.isoformat(),
            },
        }
    if unpaid_only:
        invoices = get_unpaid_invoices(db, customer_id)
    else:
        invoice = get_latest_invoice(db, customer_id)
        invoices = [invoice] if invoice else []
    if not invoices:
        return {
            "success": False,
            "error": "No invoice found.",
        }
    return {
        "success": True,
        "invoices": [
            {
                "id": invoice.id,
                "invoice_number": invoice.invoice_number,
                "amount": str(invoice.amount),
                "status": invoice.status,
                "created_at": invoice.created_at.isoformat(),
            }
            for invoice in invoices
        ],
    }