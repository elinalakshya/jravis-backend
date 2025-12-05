# src/router_health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok", "message": "JRAVIS Backend is running"}
