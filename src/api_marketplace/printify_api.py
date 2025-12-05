# src/api_marketplace/printify_api.py

import requests
from .api_manager import Keys

def printify_revenue():
    if not Keys.printify:
        return {"status": "no_key", "platform": "printify"}

    url = "https://api.printify.com/v1/shops.json"

    try:
        resp = requests.get(url, headers={"Authorization": f"Bearer {Keys.printify}"})
        if resp.status_code != 200:
            return {"status": "error", "platform": "printify"}

        shops = resp.json()
        return {
            "platform": "printify",
            "status": "ok",
            "shops": shops,
        }
    except Exception as e:
        return {"status": "error", "platform": "printify", "error": str(e)}
