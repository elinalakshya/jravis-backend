import time
import logging
import traceback

# ==========================
# Logging Setup
# ==========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("JRAVIS Worker")

# ==========================
# Import All 14 Engines
# ==========================

# OLD 6 STREAMS
from src.engines.printify_engine import run_printify_engine
from src.engines.shopify_engine import run_shopify_engine
from src.engines.export_stationery_engine import run_stationery_engine
from src.engines.gumroad_engine import run_gumroad_engine
from src.engines.payhip_engine import run_payhip_engine
from src.engines.webflow_template_engine import run_webflow_template_engine

# NEW 8 FULLY AUTOMATED STREAMS
from src.engines.auto_blogging_engine import run_auto_blogging_engine
from src.engines.affiliate_funnel_engine import run_affiliate_funnel_engine
from src.engines.pod_engine import run_pod_engine
from src.engines.template_machine_engine import run_template_machine_engine
from src.engines.multi_market_engine import run_multi_market_engine
from src.engines.dropshipping_engine import run_dropshipping_engine
from src.engines.newsletter_content_engine import run_newsletter_content_engine
from src.engines.saas_engine import run_saas_engine


# ==========================
# SAFE RUNNER WRAPPER
# ==========================
def safe_run(title, func):
    try:
        logger.info(f"🟦 Running: {title}")
        func()
        logger.info(f"✅ Completed: {title}")
    except Exception as e:
        logger.error(f"❌ Error in {title}: {e}")
        traceback.print_exc()


# ==========================
# MAIN ENGINE LOOP
# ==========================
def main():
    logger.info("💓 JRAVIS Worker Started...")
    logger.info("🔥 Running Full Engine Cycle...")

    # -------- OLD 6 STREAMS --------
    safe_run("Printify POD Engine", run_printify_engine)
    safe_run("Shopify Digital Products Engine", run_shopify_engine)
    safe_run("Stationery Export Engine", run_export_stationery_engine)
    safe_run("Gumroad Templates Engine", run_gumroad_engine)
    safe_run("Payhip Templates Engine", run_payhip_engine)
    safe_run("Webflow Template Engine", run_webflow_template_engine)

    # -------- NEW 8 AUTOMATED STREAMS --------
    safe_run("Auto Blogging Engine", run_auto_blogging_engine)
    safe_run("Affiliate Funnel Engine", run_affiliate_funnel_engine)
    safe_run("POD Mega Store Engine", run_pod_engine)
    safe_run("Template Machine Engine", run_template_machine_engine)
    safe_run("Multi-Market Uploader Engine", run_multi_market_engine)
    safe_run("Dropshipping Engine", run_dropshipping_engine)
    safe_run("Newsletter Content Engine", run_newsletter_content_engine)
    safe_run("Micro-SaaS Engine", run_saas_engine)

    logger.info("✨ ALL JRAVIS ENGINES COMPLETED SUCCESSFULLY ✨")
    logger.info("⏳ Worker sleeping for 10 minutes...")

    time.sleep(600)  # Run every 10 minutes (safe interval)


# ==========================
# START WORKER
# ==========================
if __name__ == "__main__":
    while True:
        main()
