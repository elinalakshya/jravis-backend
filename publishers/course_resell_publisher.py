import os
import logging

logger = logging.getLogger("CourseResellPublisher")

OUTPUT = "output/courses"
os.makedirs(OUTPUT, exist_ok=True)


def save_course_pack(title, lessons, materials, description):
    """
    Saves a full course pack:
    - lessons (txt files)
    - materials (pdf/txt)
    - course description
    """
    safe_title = title.replace(" ", "_").replace("/", "_")
    folder = os.path.join(OUTPUT, safe_title)
    os.makedirs(folder, exist_ok=True)

    try:
        # Save lessons
        for i, content in enumerate(lessons):
            lesson_path = os.path.join(folder, f"lesson_{i+1}.txt")
            with open(lesson_path, "w", encoding="utf-8") as f:
                f.write(content)

        # Save materials
        for name, data in materials.items():
            mat_path = os.path.join(folder, name)
            with open(mat_path, "w", encoding="utf-8") as f:
                f.write(data)

        # Save course description
        desc_path = os.path.join(folder, "description.txt")
        with open(desc_path, "w", encoding="utf-8") as f:
            f.write(description)

        logger.info(f"📘 Course Pack Saved: {folder}")
        return folder

    except Exception as e:
        logger.error(f"❌ Error saving course pack: {e}")
        return None
