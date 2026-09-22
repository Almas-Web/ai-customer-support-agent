from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class OrderCreate(BaseModel):
    item_name: str = Field(min_length=1, max_length=255)
    amount: Decimal = Field(gt=0)

class OrderResponse(BaseModel):
    id: int
    customer_id: int
    item_name: str
    amount: Decimal
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class OrderCheckoutResponse(BaseModel):
    order: OrderResponse
    payment: dict
    invoice: dict