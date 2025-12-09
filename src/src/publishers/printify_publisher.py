import os, requests, zipfile, tempfile

def publish_to_printify(title, description, file_path):
    api_key = os.getenv("PRINTIFY_API_KEY")
    shop_id = os.getenv("PRINTIFY_SHOP_ID")

    if not api_key:
        return {"ok": False, "reason": "Missing Printify API key"}

    if not shop_id:
        return {"ok": False, "reason": "Missing Printify shop ID"}

    thumb = None
    with zipfile.ZipFile(file_path, "r") as z:
        for n in z.namelist():
            if "png" in n.lower() or "jpg" in n.lower():
                tmp = tempfile.NamedTemporaryFile(delete=False)
                tmp.write(z.read(n))
                tmp.close()
                thumb = tmp.name
                break

    if thumb is None:
        return {"ok": False, "reason": "No image found in ZIP"}

    url = f"https://api.printify.com/v1/shops/{shop_id}/products.json"
    headers = {"Authorization": f"Bearer {api_key}"}

    payload = {
        "title": title,
        "description": description,
        "blueprint_id": 6,
        "print_provider_id": 1,
        "variants": [{"id": 401, "price": 1500, "is_enabled": True}],
        "images": []
    }

    r = requests.post(url, json=payload, headers=headers)

    try:
        return {"ok": r.status_code in [200, 201], "platform": "Printify", "response": r.json()}
    except:
        return {"ok": False, "response": r.text}
