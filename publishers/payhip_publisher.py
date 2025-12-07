import os
import requests

PAYHIP_API = os.getenv("PAYHIP_API_KEY", "")

def upload_to_payhip(zip_path, title):
    if not PAYHIP_API:
        return {"status": "error", "msg": "Missing Payhip API key"}

    url = "https://payhip.com/api/v1/products/create"

    try:
        with open(zip_path, "rb") as f:
            files = {"file": f}
            data = {
                "api_key": PAYHIP_API,
                "name": title,
                "price": "5.00",
            }
            r = requests.post(url, data=data, files=files)

        return {"status": "success", "response": r.json()}
    except Exception as e:
        return {"status": "error", "msg": str(e)}
