import time
import requests
import uuid
import os
from settings import (
    BACKEND_URL,
    OPENAI_API_KEY,
    PRINTIFY_API_KEY,
    MESHY_API_KEY,
    GUMROAD_TOKEN,
    PAYHIP_API_KEY
)
from publisher_printify import publish_printify_product
from publisher_gumroad import publish_gumroad_product
from publisher_payhip import publish_payhip_product
from publisher_meshy import publish_meshy_asset


def fetch_task():
    try:
        r = requests.get(f"{BACKEND_URL}/task/next")
        return r.json()
    except:
        return {"status": "error"}


def mark_done(task_id):
    try:
        requests.post(f"{BACKEND_URL}/task/done/{task_id}")
    except:
        pass


def process_publish_task(task):
    t = task["task"]
    stream = t["type"]

    print(f"🚀 Executing publish task: {stream}")

    if stream == "printify_pod":
        publish_printify_product()

    elif stream == "meshy_assets":
        publish_meshy_asset()

    elif stream == "gumroad_upload":
        publish_gumroad_product()

    elif stream == "payhip_upload":
        publish_payhip_product()

    else:
        print("⚠️ Unknown publish stream:", stream)

    print("✔ Completed:", stream)


def run_worker():
    print("🔥 JRAVIS WORKER — PUBLISH MODE ACTIVE")
    print("📡 Listening for production tasks…")

    while True:
        task = fetch_task()

        if task.get("status") == "empty":
            time.sleep(1)
            continue

        if "task" not in task:
            time.sleep(1)
            continue

        process_publish_task(task)
        mark_done(task["id"])

        time.sleep(1)

if __name__ == "__main__":
    run_worker()
