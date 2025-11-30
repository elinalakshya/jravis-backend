# worker.py

import logging
import time

from publishers.course_publisher import publish_course_material

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)

def start_worker():
    logger.info("💓 JRAVIS Worker Started...")

    while True:
        try:
            logger.info("🟦 Running course publisher task...")
            result = publish_course_material()
            logger.info(f"📨 Result: {result}")

        except Exception as e:
            logger.error(f"Worker cycle error: {e}")

        logger.info("⏳ Sleeping for 60 seconds...")
        time.sleep(60)


if __name__ == "__main__":
    start_worker()
