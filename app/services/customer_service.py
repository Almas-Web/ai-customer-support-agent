from sqlalchemy.orm import Session
from app.models.models import Customer
from app.schems.customer import CustomerCreate


def create_customer(db: Session, customer_data: CustomerCreate):
    customer = Customer(
        name=customer_data.name,
        email=customer_data.email,
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


def get_customer_by_id(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_customer_by_email(db: Session, email: str):
    return db.query(Customer).filter(Customer.email == email).first()