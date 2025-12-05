import logging
from src.engines.openai_helper import ask_openai
from publishers.affiliate_funnel_publisher import save_funnel_page

logger = logging.getLogger("AffiliateFunnelEngine")

def run_affiliate_funnel_engine():
    logger.info("🟦 Running Affiliate Funnel Engine...")

    system_prompt = """
    Create a high-conversion affiliate funnel page.
    Sections required:
    - Big promise headline
    - Emotional hook
    - Product explanation (generic)
    - 5 benefits
    - Story + transformation
    - CTA with placeholder AFFILIATE_LINK
    """

    user_prompt = "Create a funnel for a digital product (link placeholder only)."

    try:
        content = ask_openai(system_prompt, user_prompt)

        save_funnel_page(content)

        logger.info("✅ Affiliate Funnel Generated Successfully")
    except Exception as e:
        logger.error(f"❌ Affiliate Funnel Engine Error: {e}")
