import json
import os
from datetime import datetime

DRAFT_FILE = "drafts.json"


def save_draft(entry):
    drafts = []
    if os.path.exists(DRAFT_FILE):
        with open(DRAFT_FILE, "r") as f:
            drafts = json.load(f)

    drafts.insert(0, entry)

    with open(DRAFT_FILE, "w") as f:
        json.dump(drafts, f, indent=2)


def load_drafts():
    if not os.path.exists(DRAFT_FILE):
        return []
    with open(DRAFT_FILE, "r") as f:
        return json.load(f)
