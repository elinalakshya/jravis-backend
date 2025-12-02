import os
import logging

logger = logging.getLogger("AffiliateFunnelPublisher")

OUTPUT = "output/affiliate_funnels"
os.makedirs(OUTPUT, exist_ok=True)


def save_funnel_page(title, html_content):
    """Saves the affiliate funnel HTML to output folder."""
    file_name = title.replace(" ", "_").replace("/", "_") + ".html"
    file_path = os.path.join(OUTPUT, file_name)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        logger.info(f"📄 Funnel Page Saved: {file_path}")
        return file_path

    except Exception as e:
        logger.error(f"❌ Error saving funnel page: {e}")
        return None
