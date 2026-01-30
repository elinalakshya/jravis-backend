import os
from fastapi import HTTPException


def check_lock_code(provided_code: str):
    """
    Validates X-LOCK-CODE header against env variable JRAVIS_LOCK_CODE
    """

    expected_code = os.getenv("JRAVIS_LOCK_CODE")

    if not expected_code:
        raise HTTPException(
            status_code=500,
            detail="JRAVIS_LOCK_CODE is not configured on server",
        )

    if not provided_code:
        raise HTTPException(
            status_code=401,
            detail="X-LOCK-CODE header missing",
        )

    if provided_code != expected_code:
        raise HTTPException(
            status_code=403,
            detail="Invalid lock code",
        )

    return True

