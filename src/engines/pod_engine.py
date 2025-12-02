import logging
import random
from openai import OpenAI
from publishers.pod_publisher import save_pod_design

logger = logging.getLogger("PODEngine")
client = OpenAI()

POD_TOPICS = [
    "motivational quotes",
    "funny memes",
    "minimal lifestyle designs",
    "geometric patterns",
    "abstract shapes",
    "workout motivation",
    "love & romance quotes",
    "animal illustrations"
]


def generate_pod_item():
    """AI generates POD design concept + metadata."""
    topic = random.choice(POD_TOPICS)

    prompt = f"""
    Create a Print-on-Demand design concept for '{topic}'.
    Provide:
    - Title
    - Short description
    - 10 SEO tags
    - Simple text-based design placeholder (ASCII style)
    Format output as JSON:
    {{
        "title": "...",
        "description": "...",
        "tags": ["..."],
        "design": "..."
    }}
    """

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return r.choices[0].message["content"]


def run_pod_engine():
    logger.info("🎨 POD Engine Running...")

    try:
        import json
        result = generate_pod_item()
        data = json.loads(result)

        title = data["title"]
        description = data["description"]
        tags = ", ".join(data["tags"])
        design_text = data["design"]

        metadata = f"Title: {title}\nTags: {tags}\nDescription:\n{description}"

        save_pod_design(title, design_text, metadata)

        logger.info("✅ POD Asset Created Successfully")

    except Exception as e:
        logger.error(f"❌ POD Engine Error: {e}")
