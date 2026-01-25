# src/src/product_factory.py

import os
import uuid

FACTORY_DIR = "factory_output"
os.makedirs(FACTORY_DIR, exist_ok=True)


def generate_product():
    product_id = str(uuid.uuid4())[:8]

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
    price = 149  # INR

    file_path = os.path.join(FACTORY_DIR, f"planner_{product_id}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(title + "\n\n" + description)

    print("📄 TXT PRODUCT CREATED:", file_path)

    return {
        "title": title,
        "description": description,
        "price": price,
        "file_path": file_path,
    }
