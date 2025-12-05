import logging
from src.engines.openai_helper import ask_openai
from publishers.shopify_publisher import save_shopify_product

logger = logging.getLogger("ShopifyDigitalEngine")

def run_shopify_engine():
    logger.info("🟦 Running Shopify Digital Products Engine...")

    system_prompt = """
    Create a digital product for Shopify.
    Include:
    - Product title
    - Long product description
    - Features
    - File contents
    - Ideal buyer profile
    """

    user_prompt = "Generate a digital download product description."

    try:
        content = ask_openai(system_prompt, user_prompt)

        save_shopify_product(content)

        logger.info("✅ Shopify Digital Product Created Successfully")
    except Exception as e:
        logger.error(f"❌ Shopify Engine Error: {e}")
