import os
import uuid

OUTPUT_DIR = "factory_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_product():
    uid = uuid.uuid4().hex[:8]

    title = "Morning Routine Planner – Printable Productivity Toolkit"
    description = (
        "Morning Routine Planner designed to help users stay consistent,\n"
        "organized, and achieve measurable improvement.\n\n"
        "Use this planner daily:\n"
        "- Morning goals\n"
        "- Focus block\n"
        "- Reflection notes\n\n"
        "Stay consistent. Stay focused."
    )
    price = 149

    filename = f"planner_{uid}.txt"
    file_path = os.path.join(OUTPUT_DIR, filename)

    with open(file_path, "w") as f:
        f.write(title + "\n\n" + description)

    print("📄 TXT PRODUCT CREATED:", file_path)

    return {
        "title": title,
        "description": description,
        "price": price,
        "file_path": file_path,
    }
