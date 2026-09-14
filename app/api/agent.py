from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schems.agent import AgentRequest, AgentResponse
from app.agent.agent import run_agent

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.post("/chat", response_model=AgentResponse)
def chat_with_agent(
    request: AgentRequest,
    db: Session = Depends(get_db),
):
    response = run_agent(
        db=db,
        user_message=request.message,
    )

    return AgentResponse(response=response)