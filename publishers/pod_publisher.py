import os
import logging

logger = logging.getLogger("PODPublisher")

OUTPUT = "output/pod"
os.makedirs(OUTPUT, exist_ok=True)


def save_pod_design(title, artwork_text, metadata):
    """
    Creates a folder for the POD item and saves:
    - artwork placeholder (txt file)
    - metadata description
    """
    safe_title = title.replace(" ", "_").replace("/", "_")
    folder = os.path.join(OUTPUT, safe_title)
    os.makedirs(folder, exist_ok=True)

    try:
        # Save artwork placeholder file
        art_path = os.path.join(folder, "design.txt")
        with open(art_path, "w", encoding="utf-8") as f:
            f.write(artwork_text)

        # Save metadata (title, tags, description)
        meta_path = os.path.join(folder, "metadata.txt")
        with open(meta_path, "w", encoding="utf-8") as f:
            f.write(metadata)

        logger.info(f"🎨 POD Design Saved: {folder}")
        return folder

    except Exception as e:
        logger.error(f"❌ Error saving POD design: {e}")
        return None
