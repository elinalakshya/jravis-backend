import os
import logging

logger = logging.getLogger("TemplateMachinePublisher")

OUTPUT = "output/template_machines"
os.makedirs(OUTPUT, exist_ok=True)

def save_template_pack(title, files):
    """
    Saves a complete template pack:
    - Business templates
    - Notion templates
    - Resumes
    - Planners
    """
    safe = title.replace(" ", "_").replace("/", "_")
    folder = os.path.join(OUTPUT, safe)
    os.makedirs(folder, exist_ok=True)

    try:
        for filename, content in files.items():
            path = os.path.join(folder, filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

        logger.info(f"📦 Template Machine Pack Saved: {folder}")
        return folder

    except Exception as e:
        logger.error(f"❌ Error saving template machine pack: {e}")
        return None
