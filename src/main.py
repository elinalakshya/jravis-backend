# src/main.py
from fastapi import FastAPI
from src.config import settings
from src.router_health import router as health_router
from src.router_auth import router as auth_router
from src.router_streams import router as streams_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="JRAVIS Backend API for 7 Stream Automation"
)

# Attach Routers
app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(streams_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "JRAVIS Backend API Active"}
