import os
import uuid
from typing import Dict


def generate_product() -> Dict:
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

    os.makedirs("factory_output", exist_ok=True)

    filename = f"planner_{uuid.uuid4().hex[:8]}.txt"
    file_path = os.path.join("factory_output", filename)

    # ---- CREATE TXT DIGITAL PRODUCT ----
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(title + "\n\n")
        f.write(description)

    print("📄 TXT PRODUCT CREATED:", file_path)

    return {
        "zip_path": file_path,   # engine expects zip_path key
        "name": title,
        "price": price,
        "description": description,
    }

