import os
import logging

logger = logging.getLogger("DropshippingPublisher")

OUTPUT = "output/dropshipping_products"
os.makedirs(OUTPUT, exist_ok=True)

def save_dropshipping_product(title, content):
    """
    Saves product:
    - Title
    - Description
    - Tags
    - Marketing copy
    """
    safe = title.replace(" ", "_").replace("/", "_")
    folder = os.path.join(OUTPUT, safe)
    os.makedirs(folder, exist_ok=True)

    try:
        path = os.path.join(folder, "product.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"🛒 Dropshipping Product Saved: {folder}")
        return folder

    except Exception as e:
        logger.error(f"❌ Error saving dropshipping product: {e}")
        return None
