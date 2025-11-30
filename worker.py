import time
import logging

# Import all engines
from engines.printify_engine import run_printify_engine
from engines.shopify_engine import run_shopify_engine
from engines.export_stationery_engine import run_stationery_engine
from engines.gumroad_engine import run_gumroad_engine
from engines.payhip_engine import run_payhip_engine
from engines.webflow_template_engine import run_webflow_template_engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("JRAVIS-WORKER")


def run_all_streams_once():
    """
    Runs all JRAVIS income engines one by one.
    """

    logger.info("🔥 Starting Full Engine Cycle...")

    # 1. Printify POD
    try:
        run_printify_engine()
    except Exception as e:
        logger.error(f"Printify Engine Error: {e}")

    # 2. Shopify Digital Products
    try:
        run_shopify_engine()
    except Exception as e:
        logger.error(f"Shopify Engine Error: {e}")

    # 3. Stationery Export (Shopify)
    try:
        run_stationery_engine()
    except Exception as e:
        logger.error(f"Stationery Engine Error: {e}")

    # 4. Gumroad Templates
    try:
        run_gumroad_engine()
    except Exception as e:
        logger.error(f"Gumroad Engine Error: {e}")

    # 5. Payhip Templates
    try:
        run_payhip_engine()
    except Exception as e:
        logger.error(f"Payhip Engine Error: {e}")

    # 6. Webflow Templates (only works after API key)
    try:
        run_webflow_template_engine()
    except Exception as e:
        logger.error(f"Webflow Engine Error: {e}")

    logger.info("✅ Engine Cycle Completed.")


def start_worker():
    logger.info("💓 JRAVIS Worker Started...")

    while True:
        run_all_streams_once()

        logger.info("⏳ Sleeping for 60 seconds...")
        time.sleep(60)


if __name__ == "__main__":
    start_worker()
