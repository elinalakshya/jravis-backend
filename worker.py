import time
import os
import sys

# Add src/src to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(BASE_DIR, "src", "src")
sys.path.append(SRC_PATH)

print("🔧 SRC_PATH =", SRC_PATH)

from product_factory import generate_product
from unified_engine import run_all_streams_micro_engine


def run_cycle():
    print("🔥 RUNNING CYCLE")

    try:
        # 1. Generate product locally
        product = generate_product()

        # Expecting dict with zip + name
        zip_path = product.get("zip_path") or product.get("zip")
        template_name = product.get("name") or product.get("template_name")

        if not zip_path or not template_name:
            print("❌ Factory returned invalid product:", product)
            return

        print("📦 PRODUCT READY:", zip_path, template_name)

        # 2. Publish to platforms (Gumroad)
        run_all_streams_micro_engine(
            zip_path=zip_path,
            template_name=template_name,
            backend_url="local",
        )

    except Exception as e:
        print("❌ WORKER ERROR:", e)


def main():
    print("🚀 WORKER ONLINE")

    os.makedirs("factory_output", exist_ok=True)

    while True:
        run_cycle()
        time.sleep(60)  # every 1 minute


if __name__ == "__main__":
    main()

