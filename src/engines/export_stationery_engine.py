import logging
from publishers.stationery_publisher import save_stationery_product

logger = logging.getLogger(__name__)

def run_stationery_engine():
    logger.info("🟦 Running Stationery Export Engine...")

    task = {
        "type": "stationery",
        "title": "Hardcover Premium Notebook",
        "description": "AI-generated export stationery listing",
        "specs": ["Hardcover", "90 GSM paper", "A5 size"],
        "price": 8.99
    }

    try:
        save_stationery_product(task)
        logger.info("✅ Stationery export task completed.")
    except Exception as e:
        logger.error(f"❌ Stationery engine error: {e}")
