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
from src.engines.newsletter_engine import run_newsletter_engine
from src.engines.affiliate_funnel_engine import run_affiliate_funnel_engine
from src.engines.auto_blogging_engine import run_auto_blogging_engine
from src.engines.template_engine import run_template_engine
from src.engines.pod_engine import run_pod_engine
# Webflow temporarily disabled until API key arrives
# from src.engines.webflow_template_engine import run_webflow_template_engine

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

    try:
        run_printify_engine()
    except Exception as e:
        logger.error(f"❌ Printify Engine Error: {e}")

    try:
        run_shopify_engine()
    except Exception as e:
        logger.error(f"❌ Shopify Engine Error: {e}")

    try:
        run_stationery_engine()
    except Exception as e:
        logger.error(f"❌ Stationery Engine Error: {e}")

    try:
        run_gumroad_engine()
    except Exception as e:
        logger.error(f"❌ Gumroad Engine Error: {e}")

    try:
        run_payhip_engine()
    except Exception as e:
        logger.error(f"❌ Payhip Engine Error: {e}")

    try:
    run_newsletter_engine()
except Exception as e:
    logger.error(f"❌ Newsletter Engine Error: {e}")

try:
    run_affiliate_funnel_engine()
except Exception as e:
    logger.error(f"❌ Affiliate Funnel Error: {e}")

try:
    run_auto_blogging_engine()
except Exception as e:
    logger.error(f"❌ Auto Blogging Engine Error: {e}")
    
try:
    run_template_engine()
except Exception as e:
    logger.error(f"❌ Template Engine Error: {e}")

try:
    run_pod_engine()
except Exception as e:
    logger.error(f"❌ POD Engine Error: {e}")

    # Webflow disabled temporarily
    logger.info("⏳ Webflow Template Engine: Idle (waiting for API key)")

    logger.info("✅ Engine Cycle Completed.")


# -------------------------------------------------------------------
# Main Worker Loop
# -------------------------------------------------------------------
def start_worker():
    logger.info("💓 JRAVIS Worker Started...")

    while True:
        run_all_streams_once()
        logger.info("⏳ Worker sleeping for 60 seconds...")
        time.sleep(60)


# -------------------------------------------------------------------
# Worker Entry Point
# -------------------------------------------------------------------
if __name__ == "__main__":
    start_worker()
