# src/src/publishing_engine.py

import os
import logging

from publishers.gumroad_publisher import publish_to_gumroad
from publishers.printify_publisher import publish_to_printify
from publishers.payhip_publisher import publish_to_payhip

logger = logging.getLogger(__name__)


def run_publishers(title: str, description: str, zip_path: str):
    """
    Unified publisher dispatcher.
    All publishers MUST accept (title, description, zip_path).
    """
    results = []

    logger.info("📦 Publishing start: %s", title)
    logger.info("📁 ZIP path: %s", zip_path)

    if os.getenv("GUMROAD_API_KEY"):
        logger.info("➡️ Gumroad enabled")
        results.append(
            publish_to_gumroad(title, description, zip_path)
        )
    else:
        logger.info("⏭️ Gumroad skipped (no API key)")

    if os.getenv("PAYHIP_API_KEY"):
        logger.info("➡️ Payhip enabled")
        results.append(
            publish_to_payhip(title, description, zip_path)
        )
    else:
        logger.info("⏭️ Payhip skipped (no API key)")

    if os.getenv("PRINTIFY_API_KEY"):
        logger.info("➡️ Printify enabled")
        results.append(
            publish_to_printify(title, description, zip_path)
        )
    else:
        logger.info("⏭️ Printify skipped (no API key)")

    logger.info("✅ Publishing complete: %s", title)
    return results
