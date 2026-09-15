from datetime import datetime
from sqlalchemy.orm import Session
from app.models.models import Conversation, Message
def create_conversation(db: Session, customer_id: int):
    conversation = Conversation(
        customer_id=customer_id,
        status="active",
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation
def get_customer_conversations(db: Session, customer_id: int):
    return (
        db.query(Conversation)
        .filter(Conversation.customer_id == customer_id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )
def get_conversation(db: Session, conversation_id: int, customer_id: int):
    return (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.customer_id == customer_id,
        )
        .first()
    )
def add_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str,
):
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )
    db.add(message)
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    if conversation:
        conversation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(message)
    return message
def get_conversation_messages(
    db: Session,
    conversation_id: int,
):
    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )