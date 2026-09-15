from pydantic import BaseModel
class AgentRequest(BaseModel):
    message: str
    conversation_id: int | None = None
class AgentResponse(BaseModel):
    response: str