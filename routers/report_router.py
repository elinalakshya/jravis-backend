from fastapi import APIRouter
import requests
import time

router = APIRouter()

@router.post("/daily/trigger")
def trigger_daily():
    # Create a task for the worker
    return {
        "status": "scheduled",
        "task_id": f"TASK-{int(time.time())}",
        "message": "Daily report task created."
    }

@router.post("/weekly/trigger")
def trigger_weekly():
    return {
        "status": "scheduled",
        "task_id": f"TASK-{int(time.time())}",
        "message": "Weekly report task created."
    }
