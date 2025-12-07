import os
import zipfile
from pathlib import Path

# Import publisher modules
from publishers.gumroad_publisher import publish_to_gumroad
from publishers.payhip_publisher import publish_to_payhip
from publishers.printify_publisher import publish_to_printify
from publishers.newsletter_publisher import publish_to_newsletter
from publishers.affiliate_funnel_publisher import create_affiliate_funnel
from publishers.multi_marketplace_publisher import publish_to_marketplaces


# ---------------------------------------------------------
# Extract ZIP → return extracted folder path
# ---------------------------------------------------------
def extract_zip(zip_path):
    out_dir = f"unzipped/{Path(zip_path).stem}"
    os.makedirs(out_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(out_dir)

    return out_dir


# ---------------------------------------------------------
# MAIN ENGINE CALL
# ---------------------------------------------------------
def run_all_streams_micro_engine(zip_path: str, title: str):
    print("\n⚙️ JRAVIS UNIFIED ENGINE STARTED")
    print(f"📦 ZIP → {zip_path}")
    print(f"📝 Title → {title}")

    if not os.path.exists(zip_path):
        print(f"[ERROR] ZIP not found: {zip_path}")
        return {"status": "error", "reason": "zip_not_found"}

    extracted = extract_zip(zip_path)

    results = {}

    # ------------------ Gumroad ------------------
    try:
        results["gumroad"] = publish_to_gumroad(title, zip_path)
        print("[GUMROAD] OK")
    except Exception as e:
        results["gumroad"] = str(e)
        print("[GUMROAD ERROR]", e)

    # ------------------ Payhip ------------------
    try:
        results["payhip"] = publish_to_payhip(title, zip_path)
        print("[PAYHIP] OK")
    except Exception as e:
        results["payhip"] = str(e)
        print("[PAYHIP ERROR]", e)

    # ------------------ Printify ------------------
    try:
        results["printify"] = publish_to_printify(title, extracted)
        print("[PRINTIFY] OK")
    except Exception as e:
        results["printify"] = str(e)
        print("[PRINTIFY ERROR]", e)

    # ------------------ Newsletter ------------------
    try:
        results["newsletter"] = publish_to_newsletter(title, extracted)
        print("[NEWSLETTER] OK")
    except Exception as e:
        results["newsletter"] = str(e)
        print("[NEWSLETTER ERROR]", e)

    # ------------------ Funnel ------------------
    try:
        results["funnel"] = create_affiliate_funnel(title, extracted)
        print("[FUNNEL] OK")
    except Exception as e:
        results["funnel"] = str(e)
        print("[FUNNEL ERROR]", e)

    # ------------------ Marketplaces ------------------
    try:
        results["marketplaces"] = publish_to_marketplaces(title, extracted)
        print("[MARKETPLACES] OK")
    except Exception as e:
        results["marketplaces"] = str(e)
        print("[MARKETPLACES ERROR]", e)

    print("\n🎉 MONETIZATION COMPLETE\n")

    return {
        "status": "completed",
        "title": title,
        "zip": zip_path,
        "results": results,
    }
