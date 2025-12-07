# -----------------------------------------------------------
# JRAVIS Unified Monetization Engine
# Phase-1 Upload → Promotion → Funnel Generation
# -----------------------------------------------------------

import os

# Safe imports (Render-compatible)
from publishers.gumroad_publisher import upload_to_gumroad
from publishers.payhip_publisher import upload_to_payhip
from publishers.printify_publisher import upload_to_printify
from publishers.newsletter_content_publisher import send_newsletter
from publishers.affiliate_funnel_publisher import create_affiliate_funnel
from publishers.multi_marketplace_publisher import publish_to_marketplaces


# -----------------------------------------------------------
# Clean product title from ZIP filename
# -----------------------------------------------------------
def extract_title(zip_path: str) -> str:
    base = os.path.basename(zip_path)
    name = (
        base.replace(".zip", "")
            .replace("-", " ")
            .replace("_", " ")
            .title()
    )
    return name


# -----------------------------------------------------------
# JRAVIS MASTER ENGINE — RUN ALL STREAMS SAFELY
# -----------------------------------------------------------
def run_all_streams_micro_engine(zip_path: str, template_code: str):
    print("\n⚙️ JRAVIS ENGINE — Monetization Pipeline Started")
    print(f"📦 File: {zip_path}")

    title = extract_title(zip_path)
    print(f"📝 Product Title: {title}")

    # ---------------------------
    # GUMROAD
    # ---------------------------
    print("\n🚀 Gumroad Upload...")
    try:
        gumroad_res = upload_to_gumroad(zip_path, title)
    except Exception as e:
        gumroad_res = {"status": "failed", "error": str(e)}
        print("❌ Gumroad Error:", e)

    gumroad_link = None
    try:
        gumroad_link = gumroad_res.get("response", {}).get("product", {}).get("short_url")
    except:
        pass

    if not gumroad_link:
        gumroad_link = "https://gumroad.com"

    # ---------------------------
    # PAYHIP
    # ---------------------------
    print("\n🚀 Payhip Upload...")
    try:
        payhip_res = upload_to_payhip(zip_path, title)
    except Exception as e:
        payhip_res = {"status": "failed", "error": str(e)}
        print("❌ Payhip Error:", e)

    # ---------------------------
    # PRINTIFY
    # ---------------------------
    print("\n👕 Printify POD...")
    try:
        printify_res = upload_to_printify(zip_path, title)
    except Exception as e:
        printify_res = {"status": "failed", "error": str(e)}
        print("❌ Printify Error:", e)

    # ---------------------------
    # NEWSLETTER
    # ---------------------------
    print("\n📧 Newsletter Promotion...")
    try:
        newsletter_res = send_newsletter(title, gumroad_link)
    except Exception as e:
        newsletter_res = {"status": "failed", "error": str(e)}
        print("❌ Newsletter Error:", e)

    # ---------------------------
    # AFFILIATE FUNNEL
    # ---------------------------
    print("\n🌀 Affiliate Funnel Page...")
    try:
        funnel_res = create_affiliate_funnel(title, gumroad_link)
    except Exception as e:
        funnel_res = {"status": "failed", "error": str(e)}
        print("❌ Funnel Error:", e)

    # ---------------------------
    # MULTI-MARKETPLACE UPLOAD
    # ---------------------------
    print("\n🌍 Multi-Marketplace Distribution...")
    try:
        marketplace_res = publish_to_marketplaces(zip_path, title)
    except Exception as e:
        marketplace_res = {"status": "failed", "error": str(e)}
        print("❌ Marketplace Error:", e)

    # ---------------------------
    # SUMMARY
    # ---------------------------
    print("\n🎉 JRAVIS PHASE-1 MONETIZATION COMPLETE")
    print("------------------------------------")
    print("Gumroad →", gumroad_res.get("status"))
    print("Payhip →", payhip_res.get("status"))
    print("Printify →", printify_res.get("status"))
    print("Newsletter →", newsletter_res.get("status"))
    print("Funnel →", funnel_res.get("status"))
    print("Marketplaces →", marketplace_res.get("status"))
    print("------------------------------------\n")

    return {
        "gumroad": gumroad_res,
        "payhip": payhip_res,
        "printify": printify_res,
        "newsletter": newsletter_res,
        "funnel": funnel_res,
        "marketplaces": marketplace_res
    }
    
