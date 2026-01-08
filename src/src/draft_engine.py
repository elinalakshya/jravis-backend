import json
import os
from datetime import datetime
from uuid import uuid4


DRAFT_BASE_PATH = "/opt/render/project/src/data/drafts"


def ensure_dirs():
    os.makedirs(DRAFT_BASE_PATH + "/templates", exist_ok=True)


def generate_template_draft():
    """
    Generates a dummy template draft.
    Later we connect AI generation here.
    """
    draft = {
        "id": str(uuid4()),
        "stream": "template",
        "title": "Minimal Productivity Dashboard",
        "subtitle": "Track daily focus, habits, and goals",
        "description": "A clean Notion-style productivity dashboard for entrepreneurs and remote workers.",
        "features": [
            "Daily task tracker",
            "Habit monitoring",
            "Weekly review section",
            "Mobile friendly layout"
        ],
        "target_customer": "Freelancers, solopreneurs, startup founders",
        "tags": ["productivity", "notion", "dashboard", "planner"],
        "price_suggestion": "$9",
        "generated_at": datetime.utcnow().isoformat()
    }

    return draft


def save_draft(draft: dict):
    ensure_dirs()

    filename = f"{draft['id']}.json"
    filepath = f"{DRAFT_BASE_PATH}/templates/{filename}"

    with open(filepath, "w") as f:
        json.dump(draft, f, indent=2)

    return filepath


def generate_and_save_template_draft():
    draft = generate_template_draft()
    path = save_draft(draft)
    return draft, path

def generate_batch_templates(count: int = 10):
    results = []

    for _ in range(count):
        draft = generate_template_draft()
        path = save_draft(draft)
        results.append({
            "id": draft["id"],
            "title": draft["title"],
            "path": path
        })

    return results


def generate_batch_templates(count: int = 10):
    results = []

    for _ in range(count):
        draft = generate_template_draft()
        path = save_draft(draft)

        results.append({
            "id": draft["id"],
            "title": draft["title"],
            "path": path
        })

    return results
