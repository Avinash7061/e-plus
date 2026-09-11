from fastapi import FastAPI
from app.routers import auth, users, ingestion, risk
from app.routers import alerts

app = FastAPI(title="Prahari Backend")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(ingestion.router)
app.include_router(risk.router)
app.include_router(alerts.router)

@app.get("/")
def health_check():
    """Root health-check endpoint"""
    return {"status": "ok"}
