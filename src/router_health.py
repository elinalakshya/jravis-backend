# src/router_health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok", "message": "JRAVIS Backend is running"}

@router.get("/healthz")
def render_health_check():
    return {"status": "ok"}
