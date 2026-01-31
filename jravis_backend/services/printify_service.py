import os
import requests

BASE = "https://api.printify.com/v1"
API_KEY = os.getenv("PRINTIFY_API_KEY")


def upload_image(path: str) -> str:
    url = f"{BASE}/uploads/images.json"

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    with open(path, "rb") as f:
        files = {
            "file_name": (None, os.path.basename(path)),
            "contents": (os.path.basename(path), f, "image/png"),
        }

        r = requests.post(url, headers=headers, files=files)

    if r.status_code != 200:
        raise Exception(f"Printify image upload failed: {r.status_code} {r.text}")

    return r.json()["id"]

