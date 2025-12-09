import os, requests

def publish_to_gumroad(title, description, file_path):
    api_key = os.getenv("GUMROAD_API_KEY")
    if not api_key:
        return {"ok": False, "reason": "Missing Gumroad API key"}

    url = "https://api.gumroad.com/v2/products"
    payload = {
        "name": title,
        "description": description,
        "price": 0,
    }

    files = {"content": open(file_path, "rb")}

    r = requests.post(url, data=payload, files=files, params={"access_token": api_key})

    if r.status_code == 200:
        return {"ok": True, "platform": "Gumroad", "response": r.json()}
    else:
        return {"ok": False, "platform": "Gumroad", "error": r.text}
