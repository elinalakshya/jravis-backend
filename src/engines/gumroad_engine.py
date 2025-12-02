import logging
from publishers.gumroad_publisher import publish_gumroad_product

logger = logging.getLogger(__name__)

def run_gumroad_engine():
    logger.info("🟦 Running Gumroad Engine...")

    task = {
        "type": "gumroad-template",
        "title": "Instagram Carousel Pack",
        "description": "Editable Canva templates",
        "file_name": "gumroad_pack.txt"
    }

    try:
        publish_gumroad_product(task)
        logger.info("✅ Gumroad task sent.")
    except Exception as e:
        logger.error(f"❌ Gumroad engine error: {e}")
