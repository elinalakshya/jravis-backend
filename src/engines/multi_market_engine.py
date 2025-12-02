import logging
from openai import OpenAI
from publishers.multi_market_publisher import save_marketplace_pack

logger = logging.getLogger("MultiMarketEngine")
client = OpenAI()


def generate_multi_market_asset():
    """
    AI generates:
    - Title
    - Description
    - Tags list
    - 3 product files
    """
    prompt = """
    Create a digital asset pack for marketplaces (Gumroad, Creative Market, Payhip).
    Include:
    - Title
    - 15 SEO tags
    - 1 paragraph description
    - 3 files (content only, text-based)
    Format response as JSON:
    {
        "title": "...",
        "description": "...",
        "tags": ["...", "..."],
        "files": {
            "file1.txt": "...",
            "file2.txt": "...",
            "file3.txt": "..."
        }
    }
    """

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return r.choices[0].message["content"]


def run_multi_market_engine():
    logger.info("🛍 Multi-Marketplace Engine Running...")

    try:
        import json
        raw = generate_multi_market_asset()
        data = json.loads(raw)

        title = data["title"]
        desc = data["description"]
        tags = data["tags"]
        files = data["files"]

        save_marketplace_pack(title, files, desc, tags)

        logger.info("✅ Marketplace Asset Created")

    except Exception as e:
        logger.error(f"❌ Multi-Market Engine Error: {e}")
