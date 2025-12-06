# -----------------------------------------------------------
# JRAVIS — Unified Monetization Engine
# Mission 2040 — Phase-1 Full Automation
# -----------------------------------------------------------

import os
import time

# ----------------- Import Publishers -----------------------
from publishers.gumroad_publisher import publish_to_gumroad
from publishers.payhip_publisher import publish_to_payhip
from publishers.printify_publisher import publish_to_printify
from publishers.newsletter_publisher import publish_newsletter
from publishers.affiliate_funnel_publisher import publish_affiliate_funnel
from publishers.multi_marketplace_publisher import publish_to_marketplaces


# -----------------------------------------------------------
# MAIN ENGINE FUNCTION
# -----------------------------------------------------------
def run_all_streams_micro_engine(template_name, zip_path, cover_image):
    print("\n[ENGINE] ⚙️  Starting Unified Monetization Pipeline")

    results = {}

    # ----------------- 1. GUMROAD ---------------------------
    try:
        print("[ENGINE] 🚀 Uploading to Gumroad...")
        gumroad_result = publish_to_gumroad(template_name, zip_path, cover_image)
        results["gumroad"] = gumroad_result
    except Exception as e:
        print("[ENGINE] ❌ Gumroad Error:", e)
        results["gumroad"] = {"status": "error", "error": str(e)}

    # ----------------- 2. PAYHIP ----------------------------
    try:
        print("[ENGINE] 🚀 Uploading to Payhip...")
        payhip_result = publish_to_payhip(template_name, zip_path)
        results["payhip"] = payhip_result
    except Exception as e:
        print("[ENGINE] ❌ Payhip Error:", e)
        results["payhip"] = {"status": "error", "error": str(e)}

    # ----------------- 3. PRINTIFY (T-Shirt POD) ------------
    try:
        print("[ENGINE] 👕 Sending artwork to Printify...")
        printify_result = publish_to_printify(template_name, cover_image)
        results["printify"] = printify_result
    except Exception as e:
        print("[ENGINE] ❌ Printify Error:", e)
        results["printify"] = {"status": "error", "error": str(e)}

    # ----------------- 4. NEWSLETTER ------------------------
    try:
        print("[ENGINE] 📧 Sending Newsletter Blast...")
        newsletter_result = publish_newsletter(
            template_name,
            gumroad_result.get("url") if isinstance(gumroad_result, dict) else "",
            payhip_result.get("url") if isinstance(payhip_result, dict) else "",
        )
        results["newsletter"] = newsletter_result
    except Exception as e:
        print("[ENGINE] ⚠️ Newsletter Error:", e)
        results["newsletter"] = {"status": "error", "error": str(e)}

    # ----------------- 5. AFFILIATE FUNNEL -------------------
    try:
        print("[ENGINE] 🌀 Creating Affiliate Funnel Page...")
        funnel_result = publish_affiliate_funnel(
            template_name,
            gumroad_result.get("url") if isinstance(gumroad_result, dict) else "",
            payhip_result.get("url") if isinstance(payhip_result, dict) else "",
        )
        results["funnel"] = funnel_result
    except Exception as e:
        print("[ENGINE] ❌ Funnel Error:", e)
        results["funnel"] = {"status": "error", "error": str(e)}

    # ----------------- 6. MARKETPLACES -----------------------
    try:
        print("[ENGINE] 🌍 Publishing to Marketplaces...")
        marketplace_result = publish_to_marketplaces(template_name, zip_path)
        results["marketplaces"] = marketplace_result
    except Exception as e:
        print("[ENGINE] ❌ Marketplace Error:", e)
        results["marketplaces"] = {"status": "error", "error": str(e)}

    print("[ENGINE] 🎯 Monetization Cycle Completed")
    return results
