from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
import time

router = APIRouter()

# -------------------------------
# Models
# -------------------------------
class ReportRequest(BaseModel):
    mode: str  # "daily" or "weekly"


# -------------------------------
# Utility functions
# -------------------------------

def create_task(task_type: str, payload: dict):
    """
    Creates a JRAVIS task in the same style as main.py task queue.
    This function returns a dict that the worker understands.
    """
    task_id = str(uuid.uuid4())
    task = {
        "id": task_id,
        "task": {
            "type": task_type,
            **payload
        },
        "status": "pending",
        "created_at": time.time()
    }
    return task


# -------------------------------
# 1️⃣ Trigger Daily Report
# -------------------------------
@router.post("/daily/trigger")
def trigger_daily():
    """
    Triggers JRAVIS Daily Report generation task.
    Worker will generate:
        - Summary PDF (code-locked)
        - Invoice PDF
        - Email to user with approval link
    """
    from main import TASK_QUEUE  # import inside to avoid circular import

    task = create_task("daily_report", {"mode": "daily"})
    TASK_QUEUE.append(task)

    return {
        "status": "scheduled",
        "task_id": task["id"],
        "message": "Daily report task created."
    }


# -------------------------------
# 2️⃣ Trigger Weekly Report
# -------------------------------
@router.post("/weekly/trigger")
def trigger_weekly():
    """
    Triggers JRAVIS Weekly Report generation.
    """
    from main import TASK_QUEUE

    task = create_task("weekly_report", {"mode": "weekly"})
    TASK_QUEUE.append(task)

    return {
        "status": "scheduled",
        "task_id": task["id"],
        "message": "Weekly report task created."
    }


# -------------------------------
# 3️⃣ Send Report Email Manually
# -------------------------------
@router.post("/send")
def send_report_email():
    """
    Manually requests JRAVIS to send the email again with attached reports.
    Useful if the boss didn't receive the email.
    """
    from main import TASK_QUEUE

    task = create_task("send_report_email", {})
    TASK_QUEUE.append(task)

    return {
        "status": "scheduled",
        "task_id": task["id"],
        "message": "Report email send queued."
    }


# -------------------------------
# 4️⃣ Approval Endpoint
# -------------------------------
@router.get("/approve/{token}")
def approve_report(token: str):
    """
    When the boss clicks the approval link in the email,
    this endpoint is hit and JRAVIS resumes tasks.
    """
    # Very simple token validation for now
    if len(token) < 8:
        raise HTTPException(status_code=400, detail="Invalid approval token.")

    # When approved, enqueue a worker task to resume operations.
    from main import TASK_QUEUE

    task = create_task("approval_received", {"token": token})
    TASK_QUEUE.append(task)

    return {
        "status": "approved",
        "message": "Approval received. JRAVIS resuming operations.",
        "token": token
    }
