from fastapi import APIRouter, HTTPException, Header
from src.auth_manager import (
    verify_password, verify_pin, verify_lock,
    create_session, validate_session, logout
)

router = APIRouter(prefix="/auth", tags=["Auth"])

# --------------------------
# LOGIN (Password + PIN)
# --------------------------
@router.post("/login")
def login(password: str, pin: str):
    if not verify_password(password):
        raise HTTPException(status_code=401, detail="Invalid password")

    if not verify_pin(pin):
        raise HTTPException(status_code=401, detail="Invalid PIN")

    session_token = create_session()

    return {
        "success": True,
        "token": session_token,
        "message": "Login successful"
    }


# --------------------------
# SESSION VERIFICATION
# --------------------------
@router.get("/session")
def check_session(token: str = Header(None)):
    if not token or not validate_session(token):
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    return {
        "active": True,
        "message": "Session valid"
    }


# --------------------------
# LOCK CODE VERIFICATION
# --------------------------
@router.post("/lock")
def lock_verify(code: str):
    if not verify_lock(code):
        raise HTTPException(status_code=403, detail="Invalid lock code")

    return {"verified": True}


# --------------------------
# LOGOUT
# --------------------------
@router.post("/logout")
def logout_user(token: str = Header(None)):
    logout(token)
    return {"success": True, "message": "Logged out"}
