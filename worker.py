import time
import requests
from settings import BACKEND_URL

from publishers.publisher_printify import publish_printify
from publishers.publisher_payhip import publish_payhip
from publishers.publisher_gumroad import publish_gumroad
from publishers.publisher_meshy import publish_meshy
from publishers.publisher_affiliate_blog import publish_affiliate_blog
from publishers.publisher_creative_market import publish_creative_market
from publishers.publisher_stock_media import publish_stock_media
from publishers.publisher_kdp import publish_kdp
from publishers.publisher_youtube import publish_youtube
from publishers.publisher_micro_niche import publish_micro_niche
from publishers.publisher_course import publish_course

TASK_MAP = {
    "printify_pod": publish_printify,
    "payhip_upload": publish_payhip,
    "gumroad_upload": publish_gumroad,
    "meshy_assets": publish_meshy,
    "affiliate_blog": publish_affiliate_blog,
    "creative_market": publish_creative_market,
    "stock_media": publish_stock_media,
    "kdp_books": publish_kdp,
    "youtube_automation": publish_youtube,
    "micro_niche_sites": publish_micro_niche,
    "course_automation": publish_course
}

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
