import time
import requests
from settings import BACKEND_URL
from publishers.printify_publisher import publish_printify_product
from publishers.payhip_publisher import publish_payhip_product
from publishers.gumroad_publisher import publish_gumroad_product
from publishers.meshy_publisher import generate_meshy_assets
from publishers.affiliate_blog_publisher import publish_affiliate_article
from publishers.creative_market_publisher import publish_creative_market_bundle
from publishers.stock_media_publisher import publish_stock_media
from publishers.kdp_publisher import publish_kdp_book
from publishers.youtube_publisher import publish_youtube_video
from publishers.micro_niche_publisher import publish_micro_niche_site
from publishers.shopify_publisher import publish_shopify_product
from publishers.course_publisher import publish_course_content


# ----------------------------
# Fetch next task from backend
# ----------------------------
def fetch_task():
    try:
        r = requests.get(f"{BACKEND_URL}/task/next")
        return r.json()
    except:
        return {"status": "error"}


# ----------------------------
# Mark task as completed
# ----------------------------
def mark_done(task_id):
    try:
        requests.post(f"{BACKEND_URL}/task/done/{task_id}")
    except:
        pass


# ----------------------------
# ROUTER — Mapping task type → publisher
# ----------------------------
PUBLISHER_MAP = {
    "printify_pod": publish_printify_product,
    "payhip_upload": publish_payhip_product,
    "gumroad_upload": publish_gumroad_product,
    "meshy_assets": generate_meshy_assets,
    "affiliate_blog": publish_affiliate_article,
    "creative_market": publish_creative_market_bundle,
    "stock_media": publish_stock_media,
    "kdp_books": publish_kdp_book,
    "youtube_automation": publish_youtube_video,
    "micro_niche_sites": publish_micro_niche_site,
    "shopify_digital_products": publish_shopify_product,
    "course_automation": publish_course_content,
}


# ----------------------------
# MAIN WORKER LOOP
# ----------------------------
def run_worker():
    print("🚀 JRAVIS Worker Started — Ready for publishing")

    while True:
        task = fetch_task()

        # No tasks waiting
        if task.get("status") == "empty":
            time.sleep(2)
            continue

        if "task" not in task:
            time.sleep(1)
            continue

        data = task["task"]
        task_id = task["id"]
        task_type = data.get("type")

        print(f"📥 Received Task: {data}")

        # Route to correct publisher
        handler = PUBLISHER_MAP.get(task_type)

        if handler:
            try:
                success = handler(data)
                if success:
                    print("✔ Completed successfully.")
                else:
                    print("⚠ Publisher returned failure.")
            except Exception as e:
                print(f"❌ Worker Error: {e}")
        else:
            print(f"⚠ Unknown task type: {task_type}")

        # Always mark done
        mark_done(task_id)
        print(f"✔ Marked task as done: {task_id}")

        time.sleep(1)


if __name__ == "__main__":
    run_worker()
