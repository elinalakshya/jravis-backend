import logging
from publishers.shopify_publisher import publish_shopify_product

logger = logging.getLogger(__name__)

def run_shopify_engine():
    logger.info("🟦 Running Shopify Digital Product Engine...")

    task = {
        "type": "digital-product",
        "title": "Professional CV Template",
        "description": "AI-generated modern resume template.",
        "includes": ["PDF", "Canva link", "Instructions"],
        "price": 4.99
    }

    try:
        publish_shopify_product(task)
        logger.info("✅ Shopify digital product task sent.")
    except Exception as e:
        logger.error(f"❌ Shopify engine error: {e}")
