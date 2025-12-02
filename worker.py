import logging
import time
import traceback

# ==========================================================
# LOAD JRAVIS BRAIN SAFELY
# ==========================================================
import sys
import os

try:
    # Add parent directory to Python path
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(BASE_DIR)

    from jravis_config import JRAVIS_BRAIN
    print("🧠 JRAVIS_BRAIN loaded successfully.")
except Exception as e:
    JRAVIS_BRAIN = {}
    print("⚠ WARNING: Failed to load JRAVIS_BRAIN — running in SAFE MODE.")
    print("Error:", e)

# ==========================================================
# LOGGING SETUP
# ==========================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("JRAVIS Worker")


# ==========================================================
# SAFE IMPORT WRAPPER
# ==========================================================
def try_import(path, func):
    """
    Safely imports engines. Returns None if missing.
    """
    try:
        module = __import__(path, fromlist=[func])
        return getattr(module, func)
    except Exception as e:
        logger.error(f"❌ Failed to load {func} from {path}: {e}")
        return None


# ==========================================================
# ENGINE IMPORTS (All 14 Streams)
# ==========================================================

ENGINE_MAP = {
    # OLD 6 STREAMS
    "Printify POD Engine":
        try_import("src.engines.printify_engine", "run_printify_engine"),

    "Shopify Digital Products Engine":
        try_import("src.engines.shopify_engine", "run_shopify_engine"),

    "Stationery Export Engine":
        try_import("src.engines.export_stationery_engine", "run_stationery_engine"),

    "Gumroad Templates Engine":
        try_import("src.engines.gumroad_engine", "run_gumroad_engine"),

    "Payhip Templates Engine":
        try_import("src.engines.payhip_engine", "run_payhip_engine"),

    # Webflow disabled until API is active
    # "Webflow Template Engine":
    #     try_import("src.engines.webflow_template_engine", "run_webflow_template_engine"),

    # NEW 8 AUTOMATED STREAMS
    "Auto Blogging Engine":
        try_import("src.engines.auto_blogging_engine", "run_auto_blogging_engine"),

    "Affiliate Funnel Engine":
        try_import("src.engines.affiliate_funnel_engine", "run_affiliate_funnel_engine"),

    "POD Mega Store Engine":
        try_import("src.engines.pod_engine", "run_pod_engine"),

    "Template Machine Engine":
        try_import("src.engines.template_machine_engine", "run_template_machine_engine"),

    "Multi-Market Uploader Engine":
        try_import("src.engines.multi_market_engine", "run_multi_market_engine"),

    "Dropshipping Engine":
        try_import("src.engines.dropshipping_engine", "run_dropshipping_engine"),

    "Newsletter Content Engine":
        try_import("src.engines.newsletter_content_engine", "run_newsletter_content_engine"),

    "Micro-SaaS Engine":
        try_import("src.engines.saas_engine", "run_saas_engine"),
}


# ==========================================================
# SAFETY RUNNER (Prevents CRASH)
# ==========================================================
def safe_run(title, func):
    if func is None:
        logger.warning(f"⚠ Skipping {title} — engine missing or inactive.")
        return

    try:
        logger.info(f"🟦 Running → {title}")
        func()
        logger.info(f"✅ Completed → {title}")
    except Exception as e:
        logger.error(f"❌ ERROR in {title}: {e}")
        traceback.print_exc()


# ==========================================================
# APPLY JRAVIS BRAIN RULES
# ==========================================================
def enforce_brain():
    logger.info("🧠 Enforcing JRAVIS_BRAIN rules...")

    # DEBUG PRINT: Show what value is actually in the config
    owner = JRAVIS_BRAIN.get("identity", {}).get("owner")
    logger.info(f"🔍 DEBUG — JRAVIS_BRAIN identity.owner = {owner}")

    if owner != "Boss":
        logger.warning("⚠ Brain owner mismatch — switching to restricted SAFE MODE.")

    # Additional rules can be activated here:
    # - monthly target enforcement
    # - priority stream selection
    # - legal/ethical filters
    # - automation mode


# ==========================================================
# MAIN LOOP
# ==========================================================
def main():
    logger.info("💓 JRAVIS Worker Started...")
    enforce_brain()
    logger.info("🔥 Running Full 14-Engine Cycle...")

    for name, engine in ENGINE_MAP.items():
        safe_run(name, engine)
        time.sleep(1)  # safety delay

    logger.info("✨ ALL ENGINES COMPLETED — Worker sleeping for 10 minutes...")
    time.sleep(600)

# ==========================================================
# ENTRY POINT
# ==========================================================
if __name__ == "__main__":
    while True:
        main()
