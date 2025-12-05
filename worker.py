# ------------------------------------------------------
# JRAVIS WORKER v4 — Batch 8 Ready
# Handles: tasks → intelligence → sync → n8n push
# ------------------------------------------------------

import time
import requests
import random
import hashlib
import os

BACKEND = os.getenv("BACKEND_URL")
N8N_WEBHOOK = os.getenv("N8N_WEBHOOK_URL")
SECRET = os.getenv("JRAVIS_LOCK")
N8N_SECRET = os.getenv("N8N_WEBHOOK_SECRET")


# ------------------------------------------------------
# UNIQUE CONTENT GENERATOR
# ------------------------------------------------------
def generate_unique_content():
    topics = [
        "wealth creation", "global business", "ai automation",
        "productivity", "mission 2040", "ethical income"
    ]
    idea = random.choice(topics)
    tag = hashlib.sha256(str(random.random()).encode()).hexdigest()[:10]
    return f"Insight on {idea}: automation + consistency wins. #{tag}"


# ------------------------------------------------------
# DECISION LOGIC
# ------------------------------------------------------
def make_decision():
    if random.random() <= 0.60:
        return {
            "mode": "robo",
            "action": "create_content",
            "content": generate_unique_content(),
        }
    else:
        return {
            "mode": "human",
            "action": random.choice(["scroll", "review", "observe"]),
            "delay": round(random.uniform(2.5, 7.0), 2)
        }


# ------------------------------------------------------
# SEND TASK TO BACKEND
# ------------------------------------------------------
def push_task(task):
    try:
        return requests.post(
            f"{BACKEND}/api/task/new",
            json={"task": task, "lock": SECRET}
        ).json()
    except:
        return {"error": "backend unreachable"}


# ------------------------------------------------------
# PUSH DATA TO n8n (NEW)
# ------------------------------------------------------
def push_to_n8n(data):
    try:
        return requests.post(
            N8N_WEBHOOK,
            json=data,
            headers={"X-JRAVIS-SECRET": N8N_SECRET},
            timeout=10
        ).status_code
    except:
        return "failed"


# ------------------------------------------------------
# MAIN WORKER LOOP
# ------------------------------------------------------
def main():
    print("[JRAVIS] Worker Booting...")

    while True:
        print("\n--- NEW WORKER CYCLE ---")

        # 1. Decision
        decision = make_decision()
        print("🧠 Decision:", decision)

        # 2. Push task to backend
        backend_response = push_task(decision)
        print("📥 Backend Response:", backend_response)

        # 3. Push sync event to n8n
        sync = {
            "event": "worker_cycle",
            "decision": decision,
            "backend": backend_response
        }
        n8n_response = push_to_n8n(sync)
        print("🔗 N8N Sync:", n8n_response)

        # 4. Sleep
        print("⏳ Sleeping 5 minutes...")
        time.sleep(300)


if __name__ == "__main__":
    main()
