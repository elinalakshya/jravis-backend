import os, requests

def publish_to_payhip(title, description, file_path):
    api_key = os.getenv("PAYHIP_API_KEY")
    if not api_key:
        return {"ok": False, "reason": "Missing Payhip API key"}

    url = "https://payhip.com/api/v1/products"
    headers = {"Authorization": f"Bearer {api_key}"}

    files = {
        "file": open(file_path, "rb"),
    }

    data = {
        "name": title,
        "description": description,
        "price": "0",
    }

    r = requests.post(url, headers=headers, files=files, data=data)

    if r.status_code in (200, 201):
        return {"ok": True, "platform": "Payhip", "response": r.json()}
    return {"ok": False, "platform": "Payhip", "error": r.text}
