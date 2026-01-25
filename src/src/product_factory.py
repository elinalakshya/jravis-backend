import os
import uuid
from typing import Dict


OUTPUT_DIR = "factory_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


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

    price = 149  # INR

    filename = f"planner_{uuid.uuid4().hex[:8]}.txt"
    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w") as f:
        f.write(title + "\n\n" + description)

    print("📄 TXT PRODUCT CREATED:", path)

   return {
    "file_path": file_path,
    "title": title,
    "price": price
}
