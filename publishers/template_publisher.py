import os
import logging

logger = logging.getLogger("TemplatePublisher")

OUTPUT = "output/templates"
os.makedirs(OUTPUT, exist_ok=True)


def save_template_pack(title, files, description):
    """
    Saves template files + a description text.
    """
    safe_title = title.replace(" ", "_").replace("/", "_")
    folder = os.path.join(OUTPUT, safe_title)
    os.makedirs(folder, exist_ok=True)

    file_paths = []

    try:
        # Save all template files
        for filename, content in files.items():
            full_path = os.path.join(folder, filename)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            file_paths.append(full_path)

        # Save marketplace description
        desc_path = os.path.join(folder, "description.txt")
        with open(desc_path, "w", encoding="utf-8") as f:
            f.write(description)

        logger.info(f"📦 Template Pack Saved: {folder}")
        return folder, file_paths

    except Exception as e:
        logger.error(f"❌ Error saving template pack: {e}")
        return None, []
