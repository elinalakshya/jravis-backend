import time
import requests
from settings import BACKEND_URL
from publisher_printify import publish_printify_product
from publisher_gumroad import publish_gumroad_product
from publisher_payhip import publish_payhip_product
from publisher_meshy import publish_meshy_asset


def fetch_task():
    """Fetch the next task from backend"""
    try:
        r = requests.get(f"{BACKEND_URL}/task/next", timeout=10)
        return r.json()
    except Exception as e:
        print("❌ Error fetching task:", e)
        return {"status": "error"}


def mark_done(task_id):
    """Mark task finished"""
    try:
        requests.post(f"{BACKEND_URL}/task/done/{task_id}")
    except:
        pass


def process_publish_task(task):
    """Execute publishing tasks coming from JRAVIS-BRAIN"""
    t = task["task"]
    stream_type = t["type"]

    print("\n==============================")
    print(f"🚀 Executing Publish Task: {stream_type}")
    print("==============================")

    try:
        if stream_type == "printify_pod":
            result = publish_printify_product()
            print("🛍 Printify Published:", result)

        elif stream_type == "gumroad_upload":
            result = publish_gumroad_product()
            print("🛒 Gumroad Published:", result)

        elif stream_type == "payhip_upload":
            result = publish_payhip_product()
            print("💰 Payhip Published:", result)

        elif stream_type == "meshy_assets":
            result = publish_meshy_asset()
            print("🧱 Meshy Asset Generated:", result)

        else:
            print("⚠️ Unknown task type:", stream_type)
            return

    except Exception as e:
        print("❌ Publish Failed:", e)


def run_worker():
    """Main worker loop — runs 24/7"""
    print("🔥 JRAVIS WORKER — PUBLISH MODE ACTIVE")
    print("📡 Listening for publishing tasks from JRAVIS BRAIN…\n")

    while True:
        task = fetch_task()

        # If no tasks available
        if task.get("status") == "empty":
            time.sleep(2)
            continue

        # If invalid task or backend returns error
        if "task" not in task:
            time.sleep(1)
            continue

        # Process publish command
        process_publish_task(task)

        # Mark task as completed
        mark_done(task["id"])

        # Small delay before next task
        time.sleep(1)


if __name__ == "__main__":
    run_worker()
