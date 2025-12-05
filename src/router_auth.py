# src/router_auth.py
from fastapi import APIRouter, Depends
from utils.security import verify_api_key

router = APIRouter()

@router.get("/verify")
def verify_key(auth=Depends(verify_api_key)):
    return {"status": "verified", "message": "API key valid"}
