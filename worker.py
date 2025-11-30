import time
import logging
import sys
import os

# -------------------------------------------------------------------
# Ensure /src is in Python path
# -------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# -------------------------------------------------------------------
# Import Engines (correct path)
# -------------------------------------------------------------------
from src.engines.printify_engine import run_printify_engine
from src.engines.shopify_engine import run_shopify_engine
from src.engines.export_stationery_engine import run_stationery_engine
from src.engines.gumroad_engine import run_gumroad_engine
from src.engines.payhip_engine import run_payhip_engine
from src.engines.webflow_template_engine import run_webflow_template_engine

# -------------------------------------------------------------------
# Logger setup
# -------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("JRAVIS-WORKER")


# -------------------------------------------------------------------
# Run all income engines once
# -------------------------------------------------------------------
def run_all_streams_once():
    logger.info("🔥 Starting Full Engine Cycle...")

    # 1. Printify POD
    try:
        run_printify_engine()
    except Exception as e:
        logger.error(f"❌ Printify Engine Error: {e}")

    # 2. Shopify Digital Products
    try:
        run_shopify_engine()
    except Exception as e:
        logger.error(f"❌ Shopify Engine Error: {e}")

    # 3. Stationery Export (Shopify)
    try:
        run_stationery_engine()
    except Exception as e:
        logger.error(f"❌ Stationery Engine Error: {e}")

    # 4. Gumroad Templates
    try:
        run_gumroad_engine()
    except Exception as e:
        logger.error(f"❌ Gumroad Engine Error: {e}")

    # 5. Payhip Templates
    try:
        run_payhip_engine()
    except Exception as e:
        logger.error(f"❌ Payhip Engine Error: {e}")

    # 6. Webflow Templates (only works after API key arrives)
    try:
        run_webflow_template_engine()
    except Exception as e:
        logger.error(f"❌ Webflow Engine Error: {e}")

    logger.info("✅ Engine Cycle Completed.")


# -------------------------------------------------------------------
# Worker main loop
# -------------------------------------------------------------------
def start_worker():
    logger.info("💓 JRAVIS Worker Started...")

    while True:
        run_all_streams_once()
        logger.info("⏳ Worker sleeping for 60 seconds...")
        time.sleep(60)


# -------------------------------------------------------------------
# Start worker
# -------------------------------------------------------------------
if __name__ == "__main__":
    start_worker()
