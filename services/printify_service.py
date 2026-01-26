def create_printify_product(title, design_url):
    url = f"https://api.printify.com/v1/shops/{SHOP_ID}/products.json"

    data = {
        "title": title,
        "blueprint_id": 122,  # poster
        "print_provider_id": 1,
        "variants": [...],
        "print_areas": {...}
    }

    r = requests.post(url, headers=printify_headers(), json=data)
    r.raise_for_status()
