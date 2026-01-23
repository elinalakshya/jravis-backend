import traceback

from gumroad_publisher import publish_to_gumroad
from publisher_payhip import publish_to_payhip
from publisher_meshy import publish_to_meshy


def run_publishers(title: str, description: str, zip_path: str):
    print("💼 RUNNING ALL PUBLISHERS")

    results = {}

    # --------------------
    # GUMROAD (PRIMARY)
    # --------------------
    try:
        print("🟠 Publishing to Gumroad...")
        gumroad_url = publish_to_gumroad(
            title=title,
            description=description,
            price_rs=199,
            file_path=zip_path,
        )
        results["gumroad"] = gumroad_url
        print("✅ Gumroad SUCCESS:", gumroad_url)
    except Exception as e:
        print("❌ Gumroad FAILED:", e)
        traceback.print_exc()
        results["gumroad"] = None

    # --------------------
    # PAYHIP
    # --------------------
    try:
        print("🟣 Publishing to Payhip...")
        payhip_url = publish_to_payhip(title, description, zip_path)
        results["payhip"] = payhip_url
        print("✅ Payhip SUCCESS:", payhip_url)
    except Exception as e:
        print("❌ Payhip FAILED:", e)
        traceback.print_exc()
        results["payhip"] = None

    # --------------------
    # MESHY
    # --------------------
    try:
        print("🟢 Publishing to Meshy...")
        meshy_result = publish_to_meshy(title, description)
        results["meshy"] = meshy_result
        print("✅ Meshy SUCCESS")
    except Exception as e:
        print("❌ Meshy FAILED:", e)
        traceback.print_exc()
        results["meshy"] = None

    print("🏁 ALL PUBLISHERS FINISHED")
    return results

