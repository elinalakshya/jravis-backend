import logging
import time
import traceback
import requests
import sys
import os

# ==========================================================
# LOAD JRAVIS BRAIN SAFELY
# ==========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

try:
    from src.jravis_config import JRAVIS_BRAIN
    print("🧠 JRAVIS_BRAIN loaded successfully.")
except Exception as e:
    JRAVIS_BRAIN = {}
    print("⚠ WARNING: Failed to load JRAVIS_BRAIN — SAFE MODE ACTIVE")
    print("Error:", e)

# ==========================================================
# LOGGING
# ==========================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("JRAVIS Worker")


# ==========================================================
# SAFE IMPORT WRAPPER
# ==========================================================
def try_import(module_path, func_name):
    try:
        module = __import__(module_path, fromlist=[func_name])
        return getattr(module, func_name)
    except Exception as e:
        logger.error(f"❌ Failed to load {func_name} from {module_path}: {e}")
        return None


# ==========================================================
# ENGINE LIST (14 Streams)
# ==========================================================
ENGINE_MAP = {
    # ACTIVE STREAMS (7)
    "Gumroad Template Engine":
        try_import("src.engines.gumroad_engine", "run_gumroad_engine"),

    "Payhip Template Engine":
        try_import("src.engines.payhip_engine", "run_payhip_engine"),

    "Template Machine Engine":
        try_import("src.engines.template_machine_engine", "run_template_machine_engine"),

    "Auto Blogging Engine":
        try_import("src.engines.auto_blogging_engine", "run_auto_blogging_engine"),

    "Newsletter Monetization Engine":
        try_import("src.engines.newsletter_content_engine", "run_newsletter_content_engine"),

    "Affiliate Funnel Engine":
        try_import("src.engines.affiliate_funnel_engine", "run_affiliate_funnel_engine"),

    "Shopify Digital Products Engine":
        try_import("src.engines.shopify_engine", "run_shopify_engine"),

    # INACTIVE STREAMS (7)
    "Printify POD Engine":
        None,
    "Stationery Export Engine":
        None,
    "Webflow Template Engine":
        None,
    "POD Mega Store Engine":
        None,
    "Multi-Marketplace Upload Engine":
        None,
    "Dropshipping Engine":
        None,
    "Micro-SaaS Engine":
        None,
}


ACTIVE_ENGINES = [
    "Gumroad Template Engine",
    "Payhip Template Engine",
    "Template Machine Engine",
    "Auto Blogging Engine",
    "Newsletter Monetization Engine",
    "Affiliate Funnel Engine",
    "Shopify Digital Products Engine"
]


# ==========================================================
# SEND ERROR ALERT TO N8N
# ==========================================================
def send_error_to_n8n(engine, error_msg, stack):
    try:
        requests.post(
            "https://lakshyaglobal.app.n8n.cloud/webhook/jravis_error_alert",
            json={
                "engine": engine,
                "error": error_msg,
                "stacktrace": stack
            },
            timeout=5
        )
        logger.info("📨 Sent error to n8n alert workflow.")
    except Exception as alert_error:
        logger.error(f"⚠ Failed to send alert to n8n: {alert_error}")


# ==========================================================
# SAFE ENGINE RUNNER
# ==========================================================
def safe_run(title, func):
    if title not in ACTIVE_ENGINES:
        logger.info(f"⚪ {title} is inactive — skipping.")
        return

    if func is None:
        logger.warning(f"⚠ {title} engine missing.")
        return

    try:
        logger.info(f"🟦 Running → {title}")
        func()
        logger.info(f"✅ Completed → {title}")

    except Exception as e:
        logger.error(f"❌ ERROR in {title}: {e}")
        send_error_to_n8n(title, str(e), traceback.format_exc())


# ==========================================================
# APPLY JRAVIS BRAIN RULES
# ==========================================================
def enforce_brain():
    logger.info("🧠 Applying JRAVIS_BRAIN rules...")
    owner = JRAVIS_BRAIN.get("identity", {}).get("owner")
    logger.info(f"Identity check → owner = {owner}")

    if owner != "Boss":
        logger.warning("⚠ Owner mismatch → SAFE MODE")
    # Additional rules can be applied later


# ==========================================================
# MAIN LOOP
# ==========================================================
def main_cycle():
    logger.info("🔥 Running Full 14-Engine Automation Cycle...")

    for name, engine in ENGINE_MAP.items():
        safe_run(name, engine)
        time.sleep(1)

    logger.info("✨ Cycle complete. Sleeping 10 minutes...")
    time.sleep(600)


# ==========================================================
# ENTRY POINT
# ==========================================================
if __name__ == "__main__":
    logger.info("💓 JRAVIS Worker Started...")
    enforce_brain()

    while True:
        main_cycle()
