from fastapi import FastAPI
from app.api.agent import router as agent_router

app = FastAPI(title="AI Customer Support Agent")

app.include_router(agent_router)


@app.get("/")
def root():
    return {"message": "AI Customer Support Agent is running"}