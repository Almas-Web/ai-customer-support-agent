from fastapi import FastAPI

from app.api.agent import router as agent_router
from app.api.auth import router as auth_router
from app.api.customer import router as customer_router
from app.api.payment import router as payment_router
from app.api.invoice import router as invoice_router
from app.api.ticket import router as ticket_router
from app.api.conversation import router as conversation_router
from app.api.order import router as order_router

from app.db.database import SessionLocal
from app.db.seed import seed_customer_data


app = FastAPI(title="AI Customer Support Agent")


app.include_router(agent_router)
app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(payment_router)
app.include_router(invoice_router)
app.include_router(ticket_router)
app.include_router(conversation_router)
app.include_router(order_router)


@app.on_event("startup")
def startup_event():
    db = SessionLocal()

    try:
        seed_customer_data(db)
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "AI Customer Support Agent is running"}