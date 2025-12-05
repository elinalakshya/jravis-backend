# src/api_marketplace/shopify_api.py

import requests
from .api_manager import Keys

def shopify_revenue(shop_name):
    if not Keys.shopify_key or not Keys.shopify_secret:
        return {"status": "no_key", "platform": "shopify"}

    url = f"https://{shop_name}.myshopify.com/admin/api/2023-10/orders.json"

    try:
        resp = requests.get(
            url,
            auth=(Keys.shopify_key, Keys.shopify_secret),
            params={"status": "any"},
        )
        if resp.status_code != 200:
            return {"status": "error", "platform": "shopify"}

        orders = resp.json().get("orders", [])
        total = sum(float(o["total_price"]) for o in orders)

        return {
            "platform": "shopify",
            "status": "ok",
            "revenue": total,
            "orders": len(orders),
        }

    except Exception as e:
        return {"status": "error", "platform": "shopify", "error": str(e)}
