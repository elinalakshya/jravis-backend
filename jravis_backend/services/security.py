import os
from fastapi import Header, HTTPException

LOCK_CODE = os.getenv("JRAVIS_LOCK_CODE")


def verify_lock_code(x_lock_code: str = Header(None)):
    if not LOCK_CODE:
        raise HTTPException(status_code=500, detail="Lock code not configured")

    if not x_lock_code:
        raise HTTPException(status_code=401, detail="Lock code missing")

    if x_lock_code != LOCK_CODE:
        raise HTTPException(status_code=403, detail="Invalid lock code")
