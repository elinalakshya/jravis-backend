# -----------------------------------------------------------
# JRAVIS Unified Monetization Engine (FINAL)
# -----------------------------------------------------------

import os
import requests

from publishers.gumroad_publisher import publish_to_gumroad
from publishers.payhip_publisher import publish_to_payhip
from publishers.printify_publisher import publish_to_printify
from publishers.newsletter_publisher import send_newsletter
from publishers.affiliate_funnel_publisher import generate_affiliate_funnel
from publishers.multi_marketplace_publisher import publish_to_marketplaces



def run_all_streams_micro_engine(zip_path: str, title: str, backend_url: str):
    """
    FULL monetization engine.
    Now includes backend URL for downloading template ZIPs.
    """

    print("\n⚙️  JRAVIS UNIFIED ENGINE STARTED")
    print(f"📦 Input ZIP → {zip_path}")
    print(f"📝 Title → {title}")

    # -----------------------------------------------------------
    # Try downloading ZIP from backend (fixing NOT FOUND issue)
    # -----------------------------------------------------------

    if not os.path.exists(zip_path):
        download_url = f"{backend_url}/{zip_path}"
        print(f"[DOWNLOAD] Fetching: {download_url}")

        try:
            r = requests.get(download_url)
            if r.status_code == 200:
                os.makedirs("factory_output", exist_ok=True)
                with open(zip_path, "wb") as f:
                    f.write(r.content)
                print("[DOWNLOAD] ZIP saved locally.")
            else:
                print("[DOWNLOAD ERROR]", r.text)
                print("❌ ZIP Download Failed — Skipping monetization.")
                return
        except Exception as e:
            print("[DOWNLOAD EXCEPTION]", e)
            return

    # -----------------------------------------------------------
    # GUMROAD
    # -----------------------------------------------------------
    gum = publish_to_gumroad(zip_path, title)

    # -----------------------------------------------------------
    # PAYHIP
    # -----------------------------------------------------------
    pay = publish_to_payhip(zip_path, title)

    # -----------------------------------------------------------
    # PRINTIFY
    # -----------------------------------------------------------
    pod = publish_to_printify(zip_path, title)

    # -----------------------------------------------------------
    # NEWSLETTER
    # -----------------------------------------------------------
    mail = send_newsletter(title)

    # -----------------------------------------------------------
    # FUNNEL PAGE
    # -----------------------------------------------------------
    funnel = generate_affiliate_funnel(title)

    # -----------------------------------------------------------
    # MARKETPLACES
    # -----------------------------------------------------------
    market = publish_to_marketplaces(zip_path, title)

    # -----------------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------------
    print("\n🎉 MONETIZATION COMPLETE")
    print("--------------------------------------")
    print("GUMROAD →", gum)
    print("PAYHIP →", pay)
    print("PRINTIFY →", pod)
    print("NEWSLETTER →", mail)
    print("FUNNEL →", funnel)
    print("MARKETPLACES →", market)
    print("--------------------------------------\n")

    return {
        "gumroad": gum,
        "payhip": pay,
        "printify": pod,
        "newsletter": mail,
        "funnel": funnel,
        "marketplaces": market,
    }
