import logging
import time
import traceback
import sys
import os

# ==========================================================
# BOOTSTRAP PATHS & CONFIG
# ==========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

try:
    from src.jravis_config import JRAVIS_BRAIN
    print("🧠 JRAVIS_BRAIN loaded successfully.")
except Exception as e:
    JRAVIS_BRAIN = {}
    print("⚠ WARNING: JRAVIS_BRAIN failed to load — running SAFE MODE.")
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
# SAFE ENGINE IMPORT
# ==========================================================
def try_import(module_path, function_name):
    try:
        module = __import__(module_path, fromlist=[function_name])
        return getattr(module, function_name)
    except Exception as e:
        logger.error(f"❌ Failed to import {function_name} from {module_path}: {e}")
        return None


# ==========================================================
# OPENAI HELPER SHARED BY ALL ENGINES
# ==========================================================
from openai import OpenAI
client = OpenAI()

def ask_openai(system_prompt, user_prompt):
    """
    Unified helper for ALL engines.
    Safely handles new OpenAI API formats.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"❌ OpenAI Engine Error: {e}")
        return f"JRAVIS_ERROR: {e}"


# Expose helper at global level so every engine can use it
globals()["ask_openai"] = ask_openai


# ==========================================================
# ENGINE MAP (ALL 14 STREAMS)
# ==========================================================
ENGINE_MAP = {
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
# SAFE ENGINE EXECUTION WRAPPER
# ==========================================================
def safe_run(name, engine):
    if engine is None:
        logger.warning(f"⚠ Skipping {name} — Engine missing.")
        return

    try:
        logger.info(f"🔵 Running {name} ...")
        engine()
        logger.info(f"✅ Completed {name}")
    except Exception as e:
        logger.error(f"❌ ERROR in {name}: {e}")
        traceback.print_exc()


# ==========================================================
# APPLY JRAVIS BRAIN RULES
# ==========================================================
def enforce_brain():
    logger.info("🧠 Applying JRAVIS_BRAIN rules...")

    owner = JRAVIS_BRAIN.get("identity", {}).get("owner")
    logger.info(f"Identity check → owner = {owner}")

    if owner != "Boss":
        logger.warning("⚠ Unauthorized brain owner detected — SAFE MODE.")


# ==========================================================
# MAIN EXECUTION LOOP
# ==========================================================
def main():
    logger.info("💓 JRAVIS Worker Started...")
    enforce_brain()

    logger.info("🚀 Running Full 14-Engine Automation Cycle...")

    for name, engine in ENGINE_MAP.items():
        safe_run(name, engine)
        time.sleep(1)

    logger.info("🌙 Cycle complete — Sleeping 10 minutes...")
    time.sleep(600)


# ==========================================================
# ENTRY POINT
# ==========================================================
if __name__ == "__main__":
    while True:
        main()
