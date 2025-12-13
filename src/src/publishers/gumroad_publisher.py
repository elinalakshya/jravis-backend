import os
import requests

def publish_to_gumroad(title: str, description: str, zip_path: str):
    """
    Uploads ZIP product to Gumroad.
    Contract: (title, description, zip_path)
    """

    api_key = os.getenv("GUMROAD_API_KEY")
    if not api_key:
        raise RuntimeError("GUMROAD_API_KEY not set")

    if not os.path.isfile(zip_path):
        raise FileNotFoundError(f"ZIP not found: {zip_path}")

    url = "https://api.gumroad.com/v2/products"

    data = {
        "name": title,
        "description": description,
        "price": "500",  # change later
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    with open(zip_path, "rb") as f:
        files = {
            "content": f
        }

        response = requests.post(
            url,
            data=data,
            files=files,
            headers=headers,
            timeout=60,
        )

    if response.status_code not in (200, 201):
        raise RuntimeError(
            f"Gumroad upload failed [{response.status_code}]: {response.text}"
        )

    return response.json()
