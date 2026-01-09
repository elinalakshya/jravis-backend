import os
import json
import uuid
import logging
from datetime import datetime
from pathlib import Path

# -----------------------------
# Logging Setup
# -----------------------------
logging.basicConfig(level=logging.INFO)

# -----------------------------
# Storage Path
# -----------------------------
BASE_DIR = Path("/opt/render/project/src/data/drafts/templates")
BASE_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Draft Generator
# -----------------------------
def generate_template_draft():
    """
    Generates a single template draft dictionary
    """

    draft_id = str(uuid.uuid4())

    draft = {
        "id": draft_id,
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

    logging.info(f"🧠 Draft Generated | ID={draft_id} | Title={draft['title']}")

    return draft


# -----------------------------
# Save Single Draft
# -----------------------------
def generate_and_save_template_draft():
    draft = generate_template_draft()

    file_path = BASE_DIR / f"{draft['id']}.json"
    with open(file_path, "w") as f:
        json.dump(draft, f, indent=2)

    logging.info(f"💾 Draft Saved → {file_path}")

    return draft, str(file_path)


# -----------------------------
# Batch Generator
# -----------------------------
def generate_batch_templates(count: int = 10):
    """
    Generates multiple drafts in batch
    """

    results = []

    for i in range(count):
        draft, path = generate_and_save_template_draft()
        results.append({
            "id": draft["id"],
            "title": draft["title"],
            "path": path
        })

    logging.info(f"🚀 Batch Generated → {len(results)} drafts")

    return results

