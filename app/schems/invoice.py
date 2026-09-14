from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class InvoiceResponse(BaseModel):
    id: int
    customer_id: int
    invoice_number: str
    amount: Decimal
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}