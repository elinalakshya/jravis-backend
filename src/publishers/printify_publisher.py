import os, requests, json

def publish_to_printify(title, description):
    api_key = os.getenv("PRINTIFY_API_KEY")
    shop_id = os.getenv("PRINTIFY_SHOP_ID")

    if not api_key or not shop_id:
        return {"ok": False, "reason": "Missing Printify API keys"}

    url = f"https://api.printify.com/v1/shops/{shop_id}/products.json"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    body = {
        "title": title,
        "description": description,
        "blueprint_id": 6,
        "print_provider_id": 1,
        "variants": [{"id": 4012, "price": 1000, "is_enabled": True}],
        "print_areas": [],
    }

    r = requests.post(url, headers=headers, json=body)

    if r.status_code in (200, 201):
        return {"ok": True, "platform": "Printify", "response": r.json()}
    return {"ok": False, "platform": "Printify", "error": r.text}
