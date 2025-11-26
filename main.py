# JRAVIS BACKEND — MASTER API + TASK QUEUE
# Mission 2040 Core Backend

from fastapi import FastAPI
from pydantic import BaseModel
import time
import uuid

app = FastAPI()

# ------------------------------
# In-memory task queue
# ------------------------------
TASK_QUEUE = []

class Task(BaseModel):
    type: str
    mode: str | None = None
    action: str | None = None
    content: str | None = None
    count: int | None = None
    delay: float | None = None


# ------------------------------
# 1️⃣ Create new task (used by JRAVIS-BRAIN)
# ------------------------------
@app.post("/task/new")
def create_task(task: Task):
    task_id = str(uuid.uuid4())
    entry = {
        "id": task_id,
        "task": task.dict(),
        "status": "pending",
        "created_at": time.time()
    }
    TASK_QUEUE.append(entry)
    return {"status": "added", "task_id": task_id}


# ------------------------------
# 2️⃣ Worker fetches next task
# ------------------------------
@app.get("/task/next")
def next_task():
    for t in TASK_QUEUE:
        if t["status"] == "pending":
            t["status"] = "processing"
            return t
    return {"status": "empty"}


# ------------------------------
# 3️⃣ Mark task as done
# ------------------------------
@app.post("/task/done/{task_id}")
def task_done(task_id: str):
    for t in TASK_QUEUE:
        if t["id"] == task_id:
            t["status"] = "done"
            return {"status": "completed"}
    return {"status": "not_found"}


# ------------------------------
# 4️⃣ View all tasks (for daily/weekly reports)
# ------------------------------
@app.get("/task/all")
def view_all():
    return TASK_QUEUE


# ------------------------------
# 5️⃣ Health check (Render uses this)
# ------------------------------
@app.get("/healthz")
def health_check():
    return {"status": "ok"}
