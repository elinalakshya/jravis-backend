import os
from fastapi import Header, HTTPException

def verify_lock_code(x_lock_code: str = Header(None)):
    env_code = os.getenv("LOCK_CODE")

    print("HEADER:", repr(x_lock_code))
    print("ENV:", repr(env_code))

    if not x_lock_code or not env_code:
        raise HTTPException(status_code=401, detail="Invalid lock code")

    if x_lock_code.strip() != env_code.strip():
        raise HTTPException(status_code=401, detail="Invalid lock code")

