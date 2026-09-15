from sqlalchemy.orm import Session
from app.models.models import User, Customer
from app.schems.auth import RegisterRequest
from app.security import hash_password, verify_password
def register_user(db: Session, user_data: RegisterRequest):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        return None
    user = User(name=user_data.name, email=user_data.email, password_hash=hash_password(user_data.password), role="customer", is_active=True)
    db.add(user)
    db.flush()
    customer = Customer(name=user.name, email=user.email, user_id=user.id)
    db.add(customer)
    db.commit()
    db.refresh(user)
    return user
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    if not user.is_active:
        return None
    return user