import logging
from publishers.payhip_publisher import publish_payhip_product

logger = logging.getLogger(__name__)

def run_payhip_engine():
    logger.info("🟦 Running Payhip Engine...")

    task = {
        "type": "payhip-template",
        "title": "Resume Template Kit",
        "description": "AI-generated resume layouts",
        "file_name": "payhip_product.txt"
    }

    try:
        publish_payhip_product(task)
        logger.info("✅ Payhip task sent.")
    except Exception as e:
        logger.error(f"❌ Payhip engine error: {e}")
