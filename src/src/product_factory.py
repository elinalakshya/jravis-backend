# src/src/product_factory.py

import os
import uuid


OUTPUT_DIR = "factory_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_product():
    """
    Generates a simple TXT product for now.
    Later we will switch to PDF packs + ZIP.
    """

    product_id = uuid.uuid4().hex[:8]

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

    file_name = f"planner_{product_id}.txt"
    file_path = os.path.join(OUTPUT_DIR, file_name)

    content = f"""
{title}

-----------------------

{description}

-----------------------

Daily Sections:

1. Top Priority
2. Focus Task
3. Reflection
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.strip())

    print("📄 TXT PRODUCT CREATED:", file_path)

    return {
        "file_path": file_path,
        "title": title,
        "description": description,
        "price": price,
    }

