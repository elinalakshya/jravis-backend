import os, requests

def publish_to_payhip(title, description, file_path):
    api_key = os.getenv("PAYHIP_API_KEY")
    if not api_key:
        return {"ok": False, "reason": "Missing Payhip API key"}

    url = "https://payhip.com/api/v1/products/create"
    payload = {
        "name": title,
        "description": description,
        "price": 299,
    }

    files = {"file": open(file_path, "rb")}
    headers = {"Authorization": f"Bearer {api_key}"}
    r = requests.post(url, data=payload, files=files, headers=headers)

    try:
        return {"ok": r.status_code in [200, 201], "platform": "Payhip", "response": r.json()}
    except:
        return {"ok": False, "response": r.text}
