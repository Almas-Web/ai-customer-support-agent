from datetime import datetime
from pydantic import BaseModel


class TicketCreate(BaseModel):
    customer_id: int
    subject: str
    description: str
    priority: str = "medium"


class TicketResponse(BaseModel):
    id: int
    customer_id: int
    subject: str
    description: str
    status: str
    priority: str
    created_at: datetime

    model_config = {"from_attributes": True}