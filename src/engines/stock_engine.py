import logging
import random
from openai import OpenAI
from publishers.stock_publisher import save_stock_item

logger = logging.getLogger("StockEngine")
client = OpenAI()

STOCK_CATEGORIES = [
    "nature backgrounds",
    "abstract geometric patterns",
    "3D gradients",
    "minimal wallpapers",
    "cyberpunk neon scenes",
    "business lifestyle stock photos",
    "food photography setups",
    "ai futuristic backgrounds"
]


def generate_stock_media():
    """AI generates stock media concept + image prompt + keywords."""
    topic = random.choice(STOCK_CATEGORIES)

    prompt = f"""
    Create a stock media pack concept for '{topic}'.
    Provide JSON:
    {{
        "title": "...",
        "tags": ["...", "...", "..."],
        "prompt": "detailed image generation prompt"
    }}
    """

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return r.choices[0].message["content"]


def run_stock_engine():
    logger.info("🖼 Stock Media Engine Running...")

    try:
        import json
        data = generate_stock_media()
        result = json.loads(data)

        title = result["title"]
        tags = result["tags"]
        prompt = result["prompt"]

        save_stock_item(title, prompt, tags)

        logger.info("✅ Stock item generated.")

    except Exception as e:
        logger.error(f"❌ Stock Engine Error: {e}")
