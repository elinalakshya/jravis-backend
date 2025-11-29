import time
import requests
from settings import BACKEND_URL

# Import all publishers
from publishers.printify_publisher import publish_printify_product
from publishers.payhip_publisher import publish_payhip_product
from publishers.gumroad_publisher import publish_gumroad_product
from publishers.meshy_publisher import publish_meshy_assets
from publishers.affiliate_blog_publisher import publish_affiliate_blog
from publishers.creative_market_publisher import publish_creative_market
from publishers.stock_media_publisher import publish_stock_photos
from publishers.kdp_publisher import publish_kdp_book
from publishers.youtube_publisher import publish_youtube_script
from publishers.micro_niche_publisher import publish_micro_niche_site
from publishers.shopify_publisher import publish_shopify_item
from publishers.course_publisher import publish_course_material


def fetch_task():
    try:
        r = requests.get(f"{BACKEND_URL}/task/next")
        return r.json()
    except:
        return {"status": "error"}


def mark_done(task_id):
    requests.post(f"{BACKEND_URL}/task/done/{task_id}")


def run_worker():
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
        ttype = t["type"]

        try:
            print(f"📥 Received Task: {t}")

            if ttype == "printify_pod":
                publish_printify_product()

            elif ttype == "payhip_upload":
                publish_payhip_product()

            elif ttype == "gumroad_upload":
                publish_gumroad_product()

            elif ttype == "meshy_assets":
                publish_meshy_assets()

            elif ttype == "affiliate_blog":
                publish_affiliate_blog()

            elif ttype == "creative_market":
                publish_creative_market()

            elif ttype == "stock_media":
                publish_stock_photos()

            elif ttype == "kdp_books":
                publish_kdp_book()

            elif ttype == "youtube_automation":
                publish_youtube_script()

            elif ttype == "micro_niche_sites":
                publish_micro_niche_site()

            elif ttype == "shopify_digital_products":
                publish_shopify_item()

            elif ttype == "course_automation":
                publish_course_material()

            else:
                print(f"⚠ Unknown task type: {ttype}")

        except Exception as e:
            print("❌ Worker Error:", str(e))

        mark_done(task["id"])
        print(f"✔ Marked task as done: {task['id']}")

        time.sleep(1)


if __name__ == "__main__":
    run_worker()
