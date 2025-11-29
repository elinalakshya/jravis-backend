import time
import requests
from settings import BACKEND_URL

# --- Import all publishers ---
from publishers.publisher_printify import publish_printify_product
from publishers.publisher_payhip import publish_payhip_product
from publishers.publisher_gumroad import publish_gumroad_product
from publishers.publisher_meshy import publish_meshy_assets
from publishers.publisher_affiliate_blog import publish_affiliate_blog
from publishers.publisher_creative_market import publish_creative_market
from publishers.publisher_stock_media import publish_stock_media
from publishers.publisher_kdp import publish_kdp
from publishers.publisher_youtube import publish_youtube_video
from publishers.publisher_micro_niche import publish_micro_niche
from publishers.publisher_shopify import publish_shopify_product
from publishers.publisher_course import publish_course


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


# Task → Publisher mapping
PUBLISHERS = {
    "printify_pod": publish_printify_product,
    "payhip_upload": publish_payhip_product,
    "gumroad_upload": publish_gumroad_product,
    "meshy_assets": publish_meshy_assets,
    "affiliate_blog": publish_affiliate_blog,
    "creative_market": publish_creative_market,
    "stock_media": publish_stock_media,
    "kdp_books": publish_kdp,
    "youtube_automation": publish_youtube_video,
    "micro_niche_sites": publish_micro_niche,
    "shopify_digital_products": publish_shopify_product,
    "course_automation": publish_course,
}


print("🚀 JRAVIS Worker Started — Ready for publishing")

while True:
    task = fetch_task()

    if task.get("status") == "empty":
        time.sleep(2)
        continue

    if "task" not in task:
        time.sleep(1)
        continue

    t = task["task"]
    task_type = t["type"]

    try:
        if task_type in PUBLISHERS:
            print(f"📥 Received Task: {t}")
            PUBLISHERS[task_type](t)      # <— Pass the whole task
        else:
            print(f"⚠ Unknown task type: {task_type}")

    except Exception as e:
        print("❌ Worker Error:", str(e))

    finally:
        mark_done(task["id"])
        print(f"✔ Marked task as done: {task['id']}")
    time.sleep(1)
