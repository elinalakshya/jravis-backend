import os
from fastapi import APIRouter
router = APIRouter()

LOG_FILE = "/opt/render/project/src/worker.log"  # Render worker log location fallback

@router.get("/logs")
def get_logs(lines: int = 200):
    """
    Returns the last N lines of JRAVIS WORKER logs.
    Default = last 200 lines.
    """
    try:
        # If using Render, logs are not directly accessible.
        # So we maintain a custom log file inside worker.py.
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                content = f.readlines()
            return {"ok": True, "lines": content[-lines:]}

        return {"ok": False, "error": "Log file not found on server"}

    except Exception as e:
        return {"ok": False, "error": str(e)}
