# -----------------------------------------------------------
# JRAVIS Unified Monetization Engine — FINAL
# -----------------------------------------------------------

import os
import requests

# Publisher imports
from publishers.gumroad_publisher import publish_to_gumroad
from publishers.payhip_publisher import publish_to_payhip
from publishers.printify_publisher import publish_to_printify
from publishers.newsletter_publisher import send_newsletter
from publishers.affiliate_funnel_publisher import generate_affiliate_funnel
from publishers.multi_marketplace_publisher import publish_to_marketplaces


# -----------------------------------------------------------
# Helper: Extract clean title
# -----------------------------------------------------------
def extract_title(zip_path: str) -> str:
    name = os.path.basename(zip_path).replace(".zip", "")
    return name.replace("_", " ").title()


# -----------------------------------------------------------
# Download ZIP from backend
# -----------------------------------------------------------
def download_zip(backend_url, zip_path):
    url = f"{backend_url}/{zip_path}"
    print(f"[DOWNLOAD] Fetching ZIP → {url}")

    try:
        r = requests.get(url)

        if r.status_code != 200:
            print("[DOWNLOAD ERROR]", r.text)
            return None

        local_path = f"/tmp/{os.path.basename(zip_path)}"
        with open(local_path, "wb") as f:
            f.write(r.content)

        print(f"[DOWNLOAD] Saved to {local_path}")
        return local_path

    except Exception as e:
        print("[DOWNLOAD ERROR]", e)
        return None


# -----------------------------------------------------------
# MASTER ENGINE
# -----------------------------------------------------------
def run_all_streams_micro_engine(zip_path: str, title: str, backend_url: str):
    print("⚙️ JRAVIS UNIFIED ENGINE STARTED")
    print("📦 Input ZIP →", zip_path)

    clean_title = extract_title(zip_path)
    print("📝 Title →", clean_title)

    # -----------------------------------------------------------
    # STEP 1 — DOWNLOAD ZIP
    # -----------------------------------------------------------
    local_zip = download_zip(backend_url, zip_path)
    if not local_zip:
        print("❌ ZIP Download Failed — Skipping monetization.")
        return

    # -----------------------------------------------------------
    # STEP 2 — Monetization Streams
    # -----------------------------------------------------------

    # Gumroad
    print("[GUMROAD] Uploading...")
    gumroad_res = publish_to_gumroad(local_zip, clean_title)

    # Payhip
    print("[PAYHIP] Uploading...")
    payhip_res = publish_to_payhip(local_zip, clean_title)

    # Printify
    print("[PRINTIFY] Uploading POD asset...")
    printify_res = publish_to_printify(local_zip, clean_title)

    # Newsletter
    print("[NEWSLETTER] Sending campaign...")
    newsletter_res = send_newsletter(clean_title)

    # Funnel
    print("[FUNNEL] Generating...")
    funnel_res = generate_affiliate_funnel(clean_title)

    # Marketplaces
    print("[MARKETPLACES] Publishing...")
    marketplace_res = publish_to_marketplaces(local_zip, clean_title)

    print("🎉 MONETIZATION COMPLETE")

    return {
        "gumroad": gumroad_res,
        "payhip": payhip_res,
        "printify": printify_res,
        "newsletter": newsletter_res,
        "funnel": funnel_res,
        "marketplace": marketplace_res
    }
