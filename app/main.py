from fastapi import FastAPI
from app.routers import auth, users, ingestion

app = FastAPI(title="Prahari Backend")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(ingestion.router)

@app.get("/")
def health_check():
    """Root health-check endpoint"""
    return {"status": "ok"}
