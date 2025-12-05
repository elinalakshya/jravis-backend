import os
import hashlib
import secrets
from datetime import datetime, timedelta

# -----------------------------
# LOAD SECRETS FROM ENV
# -----------------------------
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")      # Boss defined
ADMIN_PIN = os.getenv("ADMIN_PIN")                # 6-digit PIN
LOCK_CODE = os.getenv("LOCK_CODE")                # JRAVIS lock

# -----------------------------
# SESSION STORAGE (memory-based)
# -----------------------------
sessions = {}  # { token: expiry_datetime }


def hash_value(value: str):
    """Hash any sensitive value."""
    return hashlib.sha256(value.encode()).hexdigest()


def verify_password(password: str):
    """Verify admin password."""
    if not ADMIN_PASSWORD:
        return False

    return hash_value(password) == hash_value(ADMIN_PASSWORD)


def verify_pin(pin: str):
    """Verify 6-digit login PIN."""
    if not ADMIN_PIN:
        return False

    return pin == ADMIN_PIN


def verify_lock(code: str):
    """Verify the JRAVIS lock code for protected actions."""
    if not LOCK_CODE:
        return False

    return code == LOCK_CODE


def create_session():
    """Generate a secure session token."""
    token = secrets.token_hex(32)
    expiry = datetime.utcnow() + timedelta(hours=12)  # Session lasts 12 hours

    sessions[token] = expiry
    return token


def validate_session(token: str):
    """Validate if session token is active."""
    if token not in sessions:
        return False

    if datetime.utcnow() > sessions[token]:
        del sessions[token]
        return False

    return True


def logout(token: str):
    """Destroy session token."""
    if token in sessions:
        del sessions[token]
