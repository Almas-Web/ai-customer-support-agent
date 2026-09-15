from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.dependencies import get_current_user
from app.models.models import Customer, User
from app.schems.conversation import ConversationResponse, MessageCreate, MessageResponse
from app.services.conversation_service import (
    create_conversation,
    get_customer_conversations,
    get_conversation,
    add_message,
    get_conversation_messages,
)
router = APIRouter(prefix="/conversations", tags=["Conversations"])
@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def create_my_conversation(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    customer = db.query(Customer).filter(
        Customer.user_id == current_user.id
    ).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer profile not found.",
        )
    return create_conversation(db, customer.id)
@router.get("", response_model=list[ConversationResponse])
def get_my_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    customer = db.query(Customer).filter(
        Customer.user_id == current_user.id
    ).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer profile not found.",
        )
    return get_customer_conversations(db, customer.id)
@router.post("/{conversation_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_my_message(
    conversation_id: int,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    customer = db.query(Customer).filter(
        Customer.user_id == current_user.id
    ).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer profile not found.",
        )
    conversation = get_conversation(
        db,
        conversation_id,
        customer.id,
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )
    if message_data.role not in ["user", "assistant"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role must be user or assistant.",
        )
    return add_message(
        db=db,
        conversation_id=conversation.id,
        role=message_data.role,
        content=message_data.content,
    )
@router.get("/{conversation_id}/messages", response_model=list[MessageResponse])
def get_my_conversation_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    customer = db.query(Customer).filter(
        Customer.user_id == current_user.id
    ).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer profile not found.",
        )
    conversation = get_conversation(
        db,
        conversation_id,
        customer.id,
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )
    return get_conversation_messages(db, conversation.id)