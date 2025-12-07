# -----------------------------------------------------------
# JRAVIS Unified Monetization Engine — FINAL STABLE VERSION
# -----------------------------------------------------------

import os
import requests

from publishers.gumroad_publisher import publish_to_gumroad
from publishers.payhip_publisher import publish_to_payhip
from publishers.printify_publisher import publish_to_printify
from publishers.newsletter_publisher import send_newsletter
from publishers.affiliate_funnel_publisher import create_funnel
from publishers.multi_marketplace_publisher import distribute_to_marketplaces


# -----------------------------------------------------------
# Extract a clean product title
# -----------------------------------------------------------
def extract_title(zip_path: str) -> str:
    base = os.path.basename(zip_path)
    clean = base.replace(".zip", "").replace("_", " ").title()
    return clean


# -----------------------------------------------------------
# Download ZIP from JRAVIS backend
# -----------------------------------------------------------
def download_zip(url: str, output_path: str) -> bool:
    try:
        print(f"[DOWNLOAD] Fetching: {url}")
        r = requests.get(url)

        if r.status_code != 200:
            print("[DOWNLOAD ERROR]", r.text)
            return False

        with open(output_path, "wb") as f:
            f.write(r.content)

        print("[DOWNLOAD] Saved:", output_path)
        return True

    except Exception as e:
        print("[DOWNLOAD ERROR]", e)
        return False


# -----------------------------------------------------------
# MAIN ENGINE — This runs ALL monetization streams
# -----------------------------------------------------------
def run_all_streams_micro_engine(zip_path: str, template_name: str, backend_url: str):
    print("\n⚙️ JRAVIS UNIFIED ENGINE STARTED")
    print("📦 Input ZIP →", zip_path)

    # Prepare product title
    title = extract_title(zip_path)
    print("📝 Title →", title)

    # Prepare local path
    local_zip = f"factory_output/{template_name}.zip"

    # Download from backend
    download_url = f"{backend_url}/{zip_path}"
    ok = download_zip(download_url, local_zip)

    if not ok:
        print("❌ ZIP Download Failed — Skipping monetization.")
        return

    # -----------------------------------------------------------
    # 1) Gumroad
    # -----------------------------------------------------------
    gumroad_res = publish_to_gumroad(local_zip, title)

    # -----------------------------------------------------------
    # 2) Payhip
    # -----------------------------------------------------------
    payhip_res = publish_to_payhip(local_zip, title)

    # -----------------------------------------------------------
    # 3) Printify POD
    # -----------------------------------------------------------
    printify_res = publish_to_printify(local_zip, title)

    # -----------------------------------------------------------
    # 4) Newsletter Blast
    # -----------------------------------------------------------
    newsletter_res = send_newsletter(title, gumroad_res.get("url"))

    # -----------------------------------------------------------
    # 5) Funnel Page
    # -----------------------------------------------------------
    funnel_res = create_funnel(title, gumroad_res.get("url"))

    # -----------------------------------------------------------
    # 6) Multi-Marketplaces
    # -----------------------------------------------------------
    market_res = distribute_to_marketplaces(local_zip, title)

    # -----------------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------------
    print("\n🎉 MONETIZATION COMPLETE")
    print("--------------------------------------")
    print("Gumroad:", gumroad_res.get("status"))
    print("Payhip:", payhip_res.get("status"))
    print("Printify:", printify_res.get("status"))
    print("Newsletter:", newsletter_res.get("status"))
    print("Funnel:", funnel_res.get("status"))
    print("Marketplace:", market_res.get("status"))
    print("--------------------------------------\n")
