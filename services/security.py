import os
from fastapi import Header, HTTPException

def verify_lock_code(x_lock_code: str = Header(None)):
    env_code = os.getenv("LOCK_CODE")

    if not env_code:
        raise HTTPException(status_code=500, detail="LOCK_CODE not set on server")

    if not x_lock_code:
        raise HTTPException(status_code=401, detail="Lock code header missing")

    if x_lock_code.strip() != env_code.strip():
        raise HTTPException(status_code=401, detail="Invalid lock code")

