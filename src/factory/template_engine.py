# src/factory/template_engine.py

import random
import hashlib
from datetime import datetime

TEMPLATE_TYPES = [
    "Webflow Template",
    "Shopify Theme",
    "Gumroad Template Pack",
    "Payhip Template Kit",
    "Funnel Landing Page",
    "Digital Planner",
    "Stationery Pack",
]

def generate_unique_seed():
    return hashlib.sha256(str(random.random()).encode()).hexdigest()[:10]


def generate_template():
    template_type = random.choice(TEMPLATE_TYPES)
    tag = generate_unique_seed()

    template = {
        "id": f"TEMP-{tag}",
        "type": template_type,
        "title": f"{template_type} — {tag}",
        "description": f"An original {template_type} created using JRAVIS Batch-9 Factory.",
        "quality_score": random.randint(70, 95),
        "created_at": datetime.utcnow().isoformat(),
    }

    return template
