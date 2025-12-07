import os
import requests

from publishers.gumroad_publisher import publish_to_gumroad
from publishers.payhip_publisher import publish_to_payhip
from publishers.printify_publisher import publish_to_printify
from publishers.newsletter_publisher import send_newsletter
from publishers.affiliate_funnel_publisher import create_affiliate_funnel
from publishers.multi_marketplace_publisher import publish_to_marketplaces


BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")


def extract_title(zip_path):
    return os.path.basename(zip_path).replace(".zip", "").title()


def run_all_streams_micro_engine(zip_path, template_name):
    print("\n⚙️ JRAVIS UNIFIED ENGINE STARTED")
    print(f"📦 Input ZIP → {zip_path}")

    title = extract_title(zip_path)
    print(f"📝 Title → {title}")

    full_url = f"{BACKEND}/{zip_path}"

    print("[DOWNLOAD] Fetching:", full_url)
    r = requests.get(full_url)

    if r.status_code != 200:
        print("[DOWNLOAD ERROR]", r.text)
        print("❌ ZIP Download Failed — Skipping monetization.")
        return

    local_zip = f"/tmp/{template_name}.zip"
    with open(local_zip, "wb") as f:
        f.write(r.content)

    # 1) Gumroad
    gum = publish_to_gumroad(local_zip, title)

    # 2) Payhip
    pay = publish_to_payhip(local_zip, title)

    # 3) Printify
    pri = publish_to_printify(local_zip, title)

    # 4) Newsletter
    news = send_newsletter(title)

    # 5) Funnel
    funnel = create_affiliate_funnel(title)

    # 6) Multi-marketplace
    market = publish_to_marketplaces(local_zip, title)

    print("🎉 MONETIZATION COMPLETE")
    return {
        "gumroad": gum,
        "payhip": pay,
        "printify": pri,
        "newsletter": news,
        "funnel": funnel,
        "marketplaces": market
    }
