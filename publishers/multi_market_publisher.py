import os
import logging

logger = logging.getLogger("MultiMarketPublisher")

OUTPUT = "output/multimarket"
os.makedirs(OUTPUT, exist_ok=True)


def save_marketplace_pack(title, files, description, tags):
    """
    Creates a folder with:
    - marketplace ready files
    - description
    - tags
    """
    safe_title = title.replace(" ", "_").replace("/", "_")
    folder = os.path.join(OUTPUT, safe_title)
    os.makedirs(folder, exist_ok=True)

    saved_files = []

    try:
        # Save file assets
        for filename, data in files.items():
            path = os.path.join(folder, filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(data)
            saved_files.append(path)

        # Save description
        desc_path = os.path.join(folder, "description.txt")
        with open(desc_path, "w", encoding="utf-8") as f:
            f.write(description)

        # Save tags
        tag_path = os.path.join(folder, "tags.txt")
        with open(tag_path, "w", encoding="utf-8") as f:
            f.write(", ".join(tags))

        logger.info(f"📦 Marketplace Pack Saved: {folder}")
        return folder, saved_files

    except Exception as e:
        logger.error(f"❌ Error saving marketplace pack: {e}")
        return None, []
