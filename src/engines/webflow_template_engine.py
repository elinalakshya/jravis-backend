import logging
from publishers.webflow_publisher import publish_webflow_template

logger = logging.getLogger(__name__)

def run_webflow_template_engine():
    logger.info("🟦 Webflow Template Engine is waiting for API key...")

    task = {
        "type": "webflow-template",
        "title": "Business Portfolio Theme",
        "html": "<div>Template layout</div>",
        "slug": "business-portfolio"
    }

    try:
        publish_webflow_template(task)
    except:
        logger.info("⏳ Webflow API key not available yet.")
