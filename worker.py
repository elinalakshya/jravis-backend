import time
import requests
import os

from settings import (
    BACKEND_URL,
    PRINTIFY_API_KEY,
    PAYHIP_API_KEY,
    GUMROAD_ACCESS_TOKEN,
    MESHY_API_KEY,
    OPENAI_API_KEY,
    OUTPUT_FOLDER    # ✅ FIXED HERE
)

# Import publishers (safe)
from publishers.printify_publisher import publish_printify_product
from publishers.payhip_publisher import publish_payhip_product
from publishers.gumroad_publisher import publish_gumroad_product
from publishers.meshy_publisher import publish_meshy_asset
from publishers.affiliate_blog_publisher import publish_affiliate_blog
from publishers.creative_market_publisher import publish_creative_market_item
from publishers.stock_media_publisher import publish_stock_media
from publishers.kdp_publisher import publish_kdp_book
from publishers.youtube_publisher import publish_youtube_video
from publishers.micro_niche_publisher import publish_micro_niche_site
from publishers.shopify_publisher import publish_shopify_product
from publishers.course_publisher import publish_course_material


print("🚀 JRAVIS Worker SAFE-PUBLISH Mode — Starting...")


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


def worker_loop():
    print("🤖 JRAVIS Worker running safely 24/7...")

    while True:
        task = fetch_task()

        if task.get("status") == "empty":
            time.sleep(2)
            continue

        if "task" not in task:
            time.sleep(1)
            continue

        t = task["task"]
        t_type = t.get("type")

        print(f"\n📥 Received Task: {t}")

        try:
            if t_type == "printify_pod":
                publish_printify_product()

            elif t_type == "payhip_upload":
                publish_payhip_product()

            elif t_type == "gumroad_upload":
                publish_gumroad_product()

            elif t_type == "meshy_assets":
                publish_meshy_asset()

            elif t_type == "affiliate_blog":
                publish_affiliate_blog()

            elif t_type == "creative_market":
                publish_creative_market_item()

            elif t_type == "stock_media":
                publish_stock_media()

            elif t_type == "kdp_books":
                publish_kdp_book()

            elif t_type == "youtube_automation":
                publish_youtube_video()

            elif t_type == "micro_niche_sites":
                publish_micro_niche_site()

            elif t_type == "shopify_digital_products":
                publish_shopify_product()

            elif t_type == "course_automation":
                publish_course_material()

            else:
                print(f"⚠ Unknown task type: {t_type}")

        except Exception as e:
            print(f"❌ Worker Error: {e}")

        mark_done(task["id"])
        print(f"✔ Marked task done: {task['id']}")

        time.sleep(3)


if __name__ == "__main__":
    worker_loop()
