import os
import logging

logger = logging.getLogger("StationeryPublisher")

OUTPUT = "output/stationery"
os.makedirs(OUTPUT, exist_ok=True)

def save_stationery_product(task):
    """
    Saves stationery product details for export.
    Works even if Shopify is not activated.
    """
    title = task.get("title", "Stationery_Product")
    safe = title.replace(" ", "_").replace("/", "_")

    folder = os.path.join(OUTPUT, safe)
    os.makedirs(folder, exist_ok=True)

    try:
        path = os.path.join(folder, "details.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("Stationery Export Product\n")
            f.write("=======================\n\n")
            f.write(f"Title: {task.get('title')}\n")
            f.write(f"Description: {task.get('description')}\n")
            f.write(f"Specs: {task.get('specs')}\n")
            f.write(f"Price: {task.get('price')}\n")

        logger.info(f"📦 Stationery Product Saved: {folder}")
        return folder

    except Exception as e:
        logger.error(f"❌ Error saving stationery product: {e}")
        return None
