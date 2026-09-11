from fastapi import FastAPI
from app.routers import auth, users, ingestion, risk
from app.routers import alerts
from contextlib import asynccontextmanager
from app.jobs.scheduler import start_scheduler, shutdown_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    shutdown_scheduler()

app = FastAPI(title="PRAHARI Backend", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(ingestion.router)
app.include_router(risk.router)
app.include_router(alerts.router)

@app.get("/")
def health_check():
    """Root health-check endpoint"""
    return {"status": "ok"}
