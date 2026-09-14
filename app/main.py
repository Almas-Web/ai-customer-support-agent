from fastapi import FastAPI

app = FastAPI(title="AI Customer Support Agent")

@app.get("/")
def root():
    return {"message": "AI Customer Support Agent is running"}