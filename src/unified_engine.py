# -----------------------------------------------------------
# JRAVIS UNIFIED ENGINE — Phase-1 Monetization Pipeline
# Connects:
#   - Gumroad Uploader
#   - Payhip Uploader
#   - Printify POD Generator
#   - Newsletter Automation
#   - Affiliate Funnel Generator
#   - Template Machine Metadata Generator
# -----------------------------------------------------------

import os
from publishers.gumroad_publisher import upload_to_gumroad
from publishers.payhip_publisher import upload_to_payhip
from publishers.printify_publisher import create_printify_product
from publishers.newsletter_content_publisher import process_newsletter
from publishers.affiliate_funnel_publisher import (
    generate_funnel_content,
    save_funnel_html
)
from publishers.template_machine_publisher import template_machine_pipeline


# ------------------------------------------------------
# Helpers
# ------------------------------------------------------

def pick_price():
    """Random price picker for templates."""
    import random
    return random.choice([5, 7, 9, 12, 15, 19, 21, 25])


def safe_log(msg):
    print(f"[ENGINE] {msg}")


# ------------------------------------------------------
# MAIN ENGINE PIPELINE
# ------------------------------------------------------

def run_all_streams_micro_engine(zip_path, base_name):
    """
    Runs ALL monetization channels after a ZIP is generated.
    """

    safe_log("⚙️  Starting Unified Monetization Pipeline")

    # --------------------------------------------------
    # 1) Generate Metadata via Template Machine
    # --------------------------------------------------
    base_title = base_name.replace("-", " ").title()
    base_description = f"A premium editable digital template named {base_title}."

    machine = template_machine_pipeline(base_title, base_description)

    if machine.get("status") != "success":
        safe_log("❌ Template Machine Error — using fallback metadata")
        metadata = {
            "title": base_title,
            "description": base_description,
            "tags": ["template", "digital", "design"]
        }
    else:
        metadata = machine["variant"]

    title = metadata["title"]
    description = metadata["description"]
    price = pick_price()

    safe_log(f"📝 Metadata Selected: {title} — ${price}")

    # --------------------------------------------------
    # 2) Upload to Gumroad
    # --------------------------------------------------
    safe_log("🚀 Uploading to Gumroad...")
    gumroad_res = upload_to_gumroad(title, description, price, zip_path)

    if gumroad_res.get("status") == "success":
        gumroad_url = gumroad_res["product_url"]
        safe_log(f"✅ Gumroad Ready: {gumroad_url}")
    else:
        gumroad_url = None
        safe_log("❌ Gumroad Upload Failed")

    # --------------------------------------------------
    # 3) Upload to Payhip
    # --------------------------------------------------
    safe_log("🚀 Uploading to Payhip...")
    payhip_res = upload_to_payhip(title, description, price, zip_path)

    if payhip_res.get("status") == "success":
        payhip_url = payhip_res["product_url"]
        safe_log(f"✅ Payhip Ready: {payhip_url}")
    else:
        payhip_url = None
        safe_log("❌ Payhip Upload Failed")

    # --------------------------------------------------
    # 4) Generate POD Product in Printify
    # --------------------------------------------------
    safe_log("👕 Sending artwork to Printify...")
    # We use either Gumroad or Payhip link as mockup reference
    mock_link = gumroad_url or payhip_url or "https://placeholder.example/template.jpg"

    pod_res = create_printify_product(title, description, mock_link)

    if pod_res.get("status") == "success":
        safe_log(f"✅ POD Product Created: {pod_res['printify_url']}")
    else:
        safe_log("❌ Printify Failed")

    # --------------------------------------------------
    # 5) Newsletter Blast
    # --------------------------------------------------
    safe_log("📧 Sending Newsletter Blast...")
    if gumroad_url:
        newsletter_res = process_newsletter(title, gumroad_url)
    elif payhip_url:
        newsletter_res = process_newsletter(title, payhip_url)
    else:
        newsletter_res = {"status": "error", "message": "No link available"}

    if newsletter_res.get("status") == "success":
        safe_log("✅ Newsletter Sent")
    else:
        safe_log("⚠️ Newsletter Error")

    # --------------------------------------------------
    # 6) Affiliate Funnel Page
    # --------------------------------------------------
    safe_log("🌀 Creating Affiliate Funnel Page...")
    funnel = generate_funnel_content(title, gumroad_url or payhip_url)

    if funnel.get("status") == "success":
        save_res = save_funnel_html(title, funnel["content"])
        safe_log(f"✅ Funnel Saved: {save_res['file']}")
    else:
        safe_log("❌ Funnel Generation Failed")

    safe_log("🎯 Monetization Cycle Completed")
