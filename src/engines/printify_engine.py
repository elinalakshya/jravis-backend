import logging
from publishers.printify_publisher import publish_printify_product

logger = logging.getLogger(__name__)

def run_printify_engine():
    logger.info("🟦 Running Printify POD Engine...")

    # The engine generates a simple POD design concept
    task = {
        "type": "pod",
        "title": "Minimalist Quote T-shirt",
        "prompt": "Generate a printable quote design with clean typography",
        "category": "apparel",
        "tags": ["quote", "minimal", "typography"]
    }

    try:
        publish_printify_product(task)
        logger.info("✅ Printify task sent successfully.")
    except Exception as e:
        logger.error(f"❌ Error in Printify engine: {e}")
