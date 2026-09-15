from datetime import datetime
from pydantic import BaseModel
class ConversationResponse(BaseModel):
    id: int
    customer_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
class MessageCreate(BaseModel):
    role: str
    content: str
class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime
    model_config = {"from_attributes": True}