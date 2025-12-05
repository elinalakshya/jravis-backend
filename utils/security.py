# utils/security.py
import os
from fastapi import HTTPException, Header

API_KEY = os.getenv("JRAVIS_API_KEY", "JRV_DEFAULT_KEY")

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")
    return True
  
