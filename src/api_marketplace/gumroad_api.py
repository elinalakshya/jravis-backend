# src/api_marketplace/gumroad_api.py

import requests
from .api_manager import Keys

BASE_URL = "https://api.gumroad.com/v2/sales"

def gumroad_revenue():
    if not Keys.gumroad:
        return {"status": "no_key", "platform": "gumroad"}

    try:
        resp = requests.get(BASE_URL, params={"access_token": Keys.gumroad})
        if resp.status_code != 200:
            return {"status": "error", "platform": "gumroad"}

        data = resp.json()
        total = sum(float(sale["price"]) / 100 for sale in data.get("sales", []))

        return {
            "platform": "gumroad",
            "status": "ok",
            "revenue": total,
            "count": len(data.get("sales", [])),
        }

    except Exception as e:
        return {"status": "error", "platform": "gumroad", "error": str(e)}
