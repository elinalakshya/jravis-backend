def create_webflow_draft(slug, name, body):
    url = f"https://api.webflow.com/collections/{COLLECTION_ID}/items"

    data = {
        "fields": {
            "name": name,
            "slug": slug,
            "content": body,
            "_draft": True,
            "_archived": False
        }
    }

    r = requests.post(url, headers=webflow_headers(), json=data)
    r.raise_for_status()
