@app.post("/api/publish/draft_all/{product_id}")
def draft_everywhere(product_id: str):

    listing = load_listing(product_id)

    gum_id = create_gumroad_product(
        listing["gumroad"]["title"],
        listing["price_inr"],
        listing["gumroad"]["description"]
    )
    upload_file(gum_id, listing["file_path"])

    create_etsy_draft(listing["etsy"])
    create_printify_product(
        listing["printify"]["title"],
        listing["printify"]["design_text"]
    )

    create_webflow_draft(
        listing["webflow"]["slug"],
        listing["title"],
        listing["webflow"]["body"]
    )

    return {"status": "drafted_everywhere"}
