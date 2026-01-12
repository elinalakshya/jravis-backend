import uuid
import random
from typing import Dict

# ---------------------------------------
# Product Idea Seeds
# ---------------------------------------

PRODUCT_IDEAS = [
    "Student Planner",
    "Daily Habit Tracker",
    "Fitness Progress Journal",
    "Budget Planner",
    "Goal Setting Workbook",
    "Meal Planning Kit",
    "Study Focus Toolkit",
    "Self Discipline Challenge",
    "Morning Routine Planner",
    "Digital Detox Planner",
]

PRICE_RANGE = [99, 149, 199, 249, 299]

TAGS = [
    "planner", "printable", "productivity", "self improvement",
    "digital download", "study", "fitness", "finance", "mindset"
]

# ---------------------------------------
# Generator
# ---------------------------------------

def generate_product() -> Dict:
    idea = random.choice(PRODUCT_IDEAS)

    title = f"{idea} – Printable Productivity Toolkit"

    description = (
        f"{idea} designed to help users stay consistent, organized, "
        f"and achieve measurable improvement. Clean printable format."
    )

    price = random.choice(PRICE_RANGE)

    sku = f"JRAVIS-{uuid.uuid4().hex[:8].upper()}"

    tags = random.sample(TAGS, k=5)

    return {
        "title": title,
        "description": description,
        "price": price,
        "tags": tags,
        "sku": sku,
    }

