import os
import logging

logger = logging.getLogger("StockPublisher")

OUTPUT = "output/stock_media"
os.makedirs(OUTPUT, exist_ok=True)


def save_stock_item(title, prompt, tags):
    """
    Saves a stock media item pack:
    - title 
    - image generation prompt
    - keyword tags
    """
    safe = title.replace(" ", "_").replace("/", "_")
    folder = os.path.join(OUTPUT, safe)
    os.makedirs(folder, exist_ok=True)

    try:
        prompt_path = os.path.join(folder, "prompt.txt")
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(prompt)

        tag_path = os.path.join(folder, "tags.txt")
        with open(tag_path, "w", encoding="utf-8") as f:
            f.write(", ".join(tags))

        logger.info(f"🖼 Stock Item Saved: {folder}")
        return folder

    except Exception as e:
        logger.error(f"❌ Error saving stock media pack: {e}")
        return None
