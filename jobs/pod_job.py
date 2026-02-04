# ==============================
# JRAVIS – PRINTIFY POD JOB
# 100% STABLE VERSION (NO AI)
# ==============================

import os
import requests
from dotenv import load_dotenv

load_dotenv()

PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY")
PRINTIFY_SHOP_ID = os.getenv("PRINTIFY_SHOP_ID")

# --------------------------------
# SAFETY CHECK
# --------------------------------
if not PRINTIFY_API_KEY or not PRINTIFY_SHOP_ID:
    raise Exception("❌ Missing PRINTIFY_API_KEY or PRINTIFY_SHOP_ID")


HEADERS = {
    "Authorization": f"Bearer {PRINTIFY_API_KEY}",
    "Content-Type": "application/json"
}


# --------------------------------
# STATIC IMAGE (NO OPENAI)
# Always works, no billing
# --------------------------------
DEFAULT_IMAGE = "https://images.printify.com/mockups/generic-shirt.png"


# --------------------------------
# CREATE SINGLE DRAFT
# --------------------------------
def create_draft(title: str, index: int):

    product_data = {
        "title": title,
        "description": "Created automatically by JRAVIS Daily Factory",
        "blueprint_id": 6,          # T-shirt (stable)
        "print_provider_id": 1,     # Default provider
        "variants": [
            {
                "id": 40171,        # safe default variant
                "price": 1999,
                "is_enabled": True
            }
        ],
        "images": [
            {
                "src": DEFAULT_IMAGE,
                "position": "front",
                "is_default": True
            }
        ],
        "is_locked": False,
        "visible": False           # IMPORTANT → stays as draft
    }

    url = f"https://api.printify.com/v1/shops/{PRINTIFY_SHOP_ID}/products.json"

    r = requests.post(url, headers=HEADERS, json=product_data)

    if r.status_code != 201:
        print("❌ Printify error:", r.text)
        return

    product = r.json()

    print(f"✅ Draft created → {product['title']} | ID: {product['id']}")


# --------------------------------
# MAIN RUN FUNCTION
# --------------------------------
def run_pod(count: int = 20):

    print("\n🚀 STARTING PRINTIFY POD FACTORY")
    print("SHOP ID =", PRINTIFY_SHOP_ID)
    print("Creating", count, "drafts...\n")

    for i in range(1, count + 1):
        title = f"Lakshya Motivation Tee #{i}"
        create_draft(title, i)

    print("\n✅ PRINTIFY POD FACTORY COMPLETED\n")


# --------------------------------
# LOCAL TEST
# --------------------------------
if __name__ == "__main__":
    run_pod(5)
