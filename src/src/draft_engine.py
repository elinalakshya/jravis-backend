import json
import uuid
import random
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

BASE_DIR = "/opt/render/project/src/data/drafts/templates"
os.makedirs(BASE_DIR, exist_ok=True)

# -------------------------------
# Knowledge pools
# -------------------------------

CATEGORIES = [
    "Productivity", "Fitness", "Finance", "Mindfulness",
    "Remote Work", "Study", "Startup", "Personal Growth"
]

PRODUCT_TYPES = [
    "Printable Planner", "Notion Template",
    "Excel Tracker", "Canva Worksheet", "Digital Toolkit"
]

TARGET_PERSONAS = [
    "Freelancers", "Startup Founders", "Students",
    "Remote Employees", "Side Hustlers", "Content Creators"
]

PROBLEMS = [
    "Poor time management",
    "Low consistency and discipline",
    "Financial tracking confusion",
    "Burnout and stress",
    "Lack of goal clarity",
    "Inefficient workflows"
]

VALUE_PROPOSITIONS = [
    "Save 5+ hours weekly",
    "Boost focus by 2x",
    "Automate daily planning",
    "Reduce mental clutter",
    "Increase execution speed",
    "Build habits effortlessly"
]

PRICE_BANDS = ["$5", "$7", "$9", "$12", "$15"]

# -------------------------------
# Core generator
# -------------------------------

def generate_draft():
    draft_id = str(uuid.uuid4())
    category = random.choice(CATEGORIES)
    product_type = random.choice(PRODUCT_TYPES)
    persona = random.choice(TARGET_PERSONAS)
    problem = random.choice(PROBLEMS)
    value = random.choice(VALUE_PROPOSITIONS)

    title = f"{category} {product_type} for {persona}"
    subtitle = f"Solves {problem.lower()} and helps you {value.lower()}"

    demand_score = random.randint(55, 95)
    competition = random.choice(["Low", "Medium", "High"])
    viral_potential = random.randint(40, 90)

    draft = {
        "id": draft_id,
        "title": title,
        "subtitle": subtitle,
        "category": category,
        "product_type": product_type,
        "target_persona": persona,
        "core_problem": problem,
        "value_proposition": value,

        "gumroad_title": title,
        "seo_description": f"{title}. Designed for {persona} to overcome {problem.lower()} and {value.lower()}.",
        "etsy_tags": [
            category.lower(),
            product_type.lower().replace(" ", "_"),
            persona.lower().replace(" ", "_"),
            "digital_download",
            "planner"
        ],

        "price_suggestion": random.choice(PRICE_BANDS),

        "market_signals": {
            "estimated_demand_score": demand_score,
            "competition_level": competition,
            "viral_potential": viral_potential,
            "upsell_ready": viral_potential > 70,
            "automation_ready": True
        },

        "created_at": datetime.utcnow().isoformat()
    }

    return draft


# -------------------------------
# Persistence
# -------------------------------

def save_draft(draft: dict):
    path = os.path.join(BASE_DIR, f"{draft['id']}.json")
    with open(path, "w") as f:
        json.dump(draft, f, indent=2)

    logging.info(f"🧠 Draft Generated | ID={draft['id']} | Title={draft['title']}")
    logging.info(f"💾 Draft Saved → {path}")
    return path


# -------------------------------
# Public APIs
# -------------------------------

def generate_and_save_template_draft():
    draft = generate_draft()
    path = save_draft(draft)
    return draft, path


def generate_batch_templates(count: int = 5):
    results = []

    for _ in range(count):
        draft = generate_draft()
        path = save_draft(draft)

        results.append({
            "id": draft["id"],
            "title": draft["title"],
            "path": path
        })

    logging.info(f"🚀 Batch Generated → {len(results)} drafts")
    return results

