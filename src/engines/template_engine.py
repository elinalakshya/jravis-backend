import logging
from openai import OpenAI
from publishers.template_publisher import save_template_pack

logger = logging.getLogger("TemplateEngine")
client = OpenAI()


def generate_template_pack():
    """
    AI generates a complete digital template + file contents.
    """
    prompt = """
    Create a digital template pack for online marketplaces (Gumroad, Payhip).
    Provide:
    - Title
    - Short description
    - 3 editable template files (content only, simple text)
    Format response as JSON:
    {
        "title": "...",
        "description": "...",
        "files": {
            "template1.txt": "...",
            "template2.txt": "...",
            "template3.txt": "..."
        }
    }
    """

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return r.choices[0].message["content"]


def run_template_engine():
    logger.info("🎨 Template Engine Running...")

    try:
        data = generate_template_pack()

        import json
        parsed = json.loads(data)

        title = parsed["title"]
        description = parsed["description"]
        files = parsed["files"]

        save_template_pack(title, files, description)

        logger.info("✅ Template Pack Created")
    except Exception as e:
        logger.error(f"❌ Template Engine Error: {e}")
