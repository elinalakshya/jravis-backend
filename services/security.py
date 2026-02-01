import os
from fastapi import Header, HTTPException

def verify_lock_code(x_lock_code: str = Header(...)):
    env_code = os.getenv("LOCK_CODE", "")

    if not x_lock_code or x_lock_code.strip() != env_code.strip():
        raise HTTPException(status_code=401, detail="Invalid lock code")

