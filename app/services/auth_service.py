from sqlalchemy.orm import Session
from app.models.models import User
from app.schems.auth import RegisterRequest
from app.security import hash_password


def register_user(db: Session, user_data: RegisterRequest):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        return None

    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role="customer",
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user