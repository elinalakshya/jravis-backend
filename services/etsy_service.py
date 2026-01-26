def create_etsy_draft(listing):
    url = f"https://openapi.etsy.com/v3/application/shops/{SHOP_ID}/listings"

    data = {
        "title": listing["title"],
        "description": listing["description"],
        "price": 5.99,
        "quantity": 999,
        "who_made": "i_did",
        "when_made": "made_to_order",
        "taxonomy_id": 69150433,
        "tags": listing["tags"],
        "state": "draft"
    }

    r = requests.post(url, headers=etsy_headers(), json=data)
    r.raise_for_status()
