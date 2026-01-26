import os
import requests

WEBFLOW_TOKEN = os.getenv("WEBFLOW_TOKEN")
WEBFLOW_COLLECTION_ID = os.getenv("WEBFLOW_COLLECTION_ID")


def _headers():
    return {
        "Authorization": f"Bearer {WEBFLOW_TOKEN}",
        "Content-Type": "application/json",
        "accept-version": "1.0.0"
    }


def create_draft_item(slug, name, body):
    url = f"https://api.webflow.com/collections/{WEBFLOW_COLLECTION_ID}/items"

    data = {
        "fields": {
            "name": name,
            "slug": slug,
            "content": body,
            "_draft": True,
            "_archived": False
        }
    }

    r = requests.post(url, headers=_headers(), json=data, timeout=60)
    r.raise_for_status()
