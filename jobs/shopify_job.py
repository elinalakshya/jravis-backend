import os, requests
from dotenv import load_dotenv

load_dotenv()
STORE = os.getenv("SHOPIFY_STORE")
TOKEN = os.getenv("SHOPIFY_TOKEN")

def run_shopify(count=10):
    for i in range(count):
        requests.post(
            f"https://{STORE}/admin/api/2024-01/products.json",
            headers={"X-Shopify-Access-Token": TOKEN},
            json={
                "product": {
                    "title": f"Digital Planner #{i+1}",
                    "status": "draft"
                }
            }
        )
